from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import re
import sys
import errno
import shutil
import base64
import mimetypes
import threading
from traceback import format_exc

import requests
from flask import (
    Flask, abort, make_response, render_template, request, safe_join,
    send_from_directory, url_for)

from . import __version__
from .constants import default_filenames
from .renderer import render_content
from .browser import wait_and_start_browser

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin


def create_app(path=None, gfm=False, context=None,
               username=None, password=None,
               render_offline=False, render_wide=False, render_inline=False,
               text=None, api_url=None, title=None):
    """
    Creates an WSGI application that can serve the specified file or
    directory containing a README.
    """

    use_stdin = path == '-' and text is None
    if path == '-':
        path = None

    force_resolve = text is not None or use_stdin
    in_filename = resolve_readme(path, force_resolve)

    # Create Flask application
    app = _create_flask()

    if use_stdin:
        # Handle debug mode special case
        if app.config['DEBUG_GRIP']:
            text = (os.environ['GRIP_STDIN_TEXT']
                    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
                    else sys.stdin.read())
            if not os.environ.get('WERKZEUG_RUN_MAIN'):
                os.environ['GRIP_STDIN_TEXT'] = text
        else:
            text = sys.stdin.read()

    # Runtime config
    cache_directory = _cache_directory(app)
    username = username if username is not None else app.config.get('USERNAME')
    password = password if password is not None else app.config.get('PASSWORD')
    api_url = api_url if api_url is not None else app.config.get('API_URL')

    # Authentication message
    is_authenticated = bool(username) or bool(password)
    if is_authenticated:
        if username:
            print(' * Using credentials:', username, file=sys.stderr)
        else:
            print(' * Using personal access token', file=sys.stderr)

    # Setup style cache
    cache_path = (os.path.join(app.instance_path, cache_directory)
                  if cache_directory
                  else None)
    cache_url = app.config.get('CACHE_URL')

    # Get initial assets
    assets = {}
    style_urls = list(app.config['STYLE_URLS'] or [])
    styles = []

    # Get styles from style source
    @app.before_first_request
    def retrieve_styles():
        """
        Retrieves the style URLs from the source and caches them.
        """
        style_urls_source = app.config['STYLE_URLS_SOURCE']
        style_urls_re = app.config['STYLE_URLS_RE']
        if not style_urls_source or not style_urls_re:
            return

        # Get style URLs from the source HTML page
        retrieved_urls = _get_style_urls(style_urls_source,
                                         style_urls_re,
                                         app.config['STYLE_ASSET_URLS_RE'],
                                         app.config['STYLE_ASSET_URLS_SUB'],
                                         cache_path,
                                         app.config['DEBUG_GRIP'])
        style_urls.extend(retrieved_urls)

        if render_inline:
            favicon_url = url_for('static', filename='favicon.ico')
            assets['favicon'] = _to_data_url(app, favicon_url, 'image/x-icon')
            styles.extend(_get_styles(app, style_urls,
                                      app.config['STYLE_ASSET_URLS_INLINE']))
            style_urls[:] = []

    # Views
    @app.route('/')
    @app.route('/<path:filename>')
    def render(filename=None):
        if filename is not None:
            filename = safe_join(os.path.dirname(in_filename), filename)
            if os.path.isdir(filename):
                filename = _find_file_or_404(filename, force_resolve)
            # Read and serve images as binary
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype and mimetype.startswith('image/'):
                image_data = _read_file_or_404(filename, False)
                return _render_image(image_data, mimetype)
            render_text = _read_file_or_404(filename)
        else:
            filename = in_filename
            if text is not None:
                render_text = (text.read() if hasattr(text, 'read')
                               else str(text))
            else:
                render_text = _read_file_or_404(filename)

        favicon = assets.get('favicon', None)

        return _render_page(render_text, filename, gfm, context,
                            username, password,
                            render_offline, render_wide,
                            style_urls, styles, favicon, api_url,
                            title)

    @app.route(cache_url + '/octicons/octicons/<filename>')
    def render_octicon(filename=None):
        return send_from_directory(cache_path, filename)

    @app.route(cache_url + '/<path:filename>')
    def render_cache(filename=None):
        return send_from_directory(cache_path, filename)

    # Error views
    @app.route('/rate-limit-preview')
    @app.errorhandler(403)
    def rate_limit_preview(exception=None):
        auth = request.args.get('auth')
        is_auth = auth == '1' if auth else is_authenticated
        return render_template('limit.html', is_authenticated=is_auth), 403

    return app


def serve(path=None, host=None, port=None, gfm=False, context=None,
          username=None, password=None,
          render_offline=False, render_wide=False, render_inline=False,
          api_url=None, browser=False, title=None):
    """
    Starts a server to render the specified file
    or directory containing a README.
    """
    app = create_app(path, gfm, context, username, password,
                     render_offline, render_wide, render_inline, None, api_url,
                     title)

    # Set overridden config values
    if host is not None:
        app.config['HOST'] = host
    if port is not None:
        app.config['PORT'] = port

    # Opening browser
    if browser:
        browser_thread = threading.Thread(
            target=wait_and_start_browser,
            args=(app.config['HOST'], app.config['PORT']))
        browser_thread.start()

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.debug,
            use_reloader=app.config['DEBUG_GRIP'])

    # Closing browser
    if browser:
        browser_thread.join()


def clear_cache():
    """
    Clears the cached styles and assets.
    """
    app = _create_flask()
    cache_path = os.path.join(app.instance_path, _cache_directory(app))
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    print('Cache cleared.')


def resolve_readme(path=None, force=False):
    """
    Returns the path if it's a file; otherwise, looks for a compatible
    README file in the directory specified by path. If path is None,
    the current working directory is used. If no compatible README can
    be found, a ValueError is raised.
    """
    if not path or os.path.isdir(path):
        path = _find_file(path, force)
    if not os.path.exists(path) and not force:
        raise ValueError('File not found: ' + path)
    return os.path.normpath(path)


def _create_flask():
    if 'GRIPHOME' in os.environ:
        instance_path = os.environ['GRIPHOME']
    else:
        instance_path = os.path.abspath(os.path.expanduser('~/.grip'))
    user_settings = os.path.join(instance_path, 'settings.py')
    default_static_url_path = '/grip-static'

    # Flask application
    def _new_flask(static_url_path=default_static_url_path):
        app = Flask(__name__,
                    static_url_path=static_url_path,
                    instance_path=instance_path)
        app.config.from_object('grip.settings')
        app.config.from_pyfile('settings_local.py', silent=True)
        app.config.from_pyfile(user_settings, silent=True)
        return app

    app = _new_flask()
    static_url_path = app.config['STATIC_URL_PATH']
    if static_url_path and static_url_path != default_static_url_path:
        app = _new_flask(static_url_path)

    return app


def _cache_directory(app):
    """
    Gets the cache directory for the specified app.
    """
    return app.config['CACHE_DIRECTORY'].format(version=__version__)


def _render_page(text, filename=None, gfm=False, context=None,
                 username=None, password=None,
                 render_offline=False, render_wide=False,
                 style_urls=[], styles=[], favicon=None, api_url=None,
                 title=None):
    """
    Renders the specified markup text to an HTML page.
    """
    render_title = not gfm
    content = render_content(text, gfm, context, username, password,
                             render_offline, api_url)

    if title is None:
        title = filename

    return render_template('index.html',
                           content=content, filename=filename,
                           render_wide=render_wide,
                           style_urls=style_urls, styles=styles,
                           favicon=favicon,
                           render_title=render_title,
                           discussion=gfm,
                           title=title)


def _render_image(image_data, content_type):
    """
    Renders the specified image data with the given Content-Type.
    """
    response = make_response(image_data)
    response.headers['Content-Type'] = content_type
    return response


def _get_style_urls(source_url, style_pattern, asset_pattern,
                    asset_pattern_sub, cache_path, debug=False):
    """
    Gets the specified resource and parses all style URLs and their
    assets in the form of the specified patterns.
    """
    try:
        # Check cache
        if cache_path:
            cached = _get_cached_style_urls(cache_path)
            # Skip fetching styles if there's any already cached
            if cached:
                return cached

        # Find style URLs
        r = requests.get(source_url)
        if not 200 <= r.status_code < 300:
            print('Warning: retrieving styles gave status code',
                  r.status_code, file=sys.stderr)
        urls = re.findall(style_pattern, r.text)

        # Cache the styles and their assets
        if cache_path:
            is_cached = _cache_contents(urls, asset_pattern, asset_pattern_sub,
                                        cache_path)
            if is_cached:
                urls = _get_cached_style_urls(cache_path)

        return urls
    except Exception as ex:
        if debug:
            print(format_exc(), file=sys.stderr)
        else:
            print(' * Error: could not retrieve styles:', ex, file=sys.stderr)
        return []


def _get_styles(app, style_urls, asset_pattern):
    """
    Gets the content of the given list of style URLs and
    inlines assets.
    """
    styles = []
    for style_url in style_urls:

        def match_asset(match):
            url = urljoin(style_url, _normalize_url(match.group(1)))
            ext = os.path.splitext(url)[1][1:]
            return 'url({0})'.format(_to_data_url(app, url, 'font/' + ext))

        content = re.sub(asset_pattern, match_asset, _download(app, style_url))
        styles.append(content)

    return styles


def _to_data_url(app, url, content_type):
    asset = _download(app, url, binary=True)
    asset64_bytes = base64.b64encode(asset)
    asset64_string = asset64_bytes.decode('ascii')
    return 'data:{0};base64,{1}'.format(content_type, asset64_string)


def _download(app, url, binary=False):
    if urlparse(url).netloc:
        r = requests.get(url)
        return r.content if binary else r.text

    with app.test_client() as c:
        r = c.get(url)
        charset = r.mimetype_params.get('charset', 'utf-8')
        data = c.get(url).data
        return data if binary else data.decode(charset)


def _get_cached_style_urls(cache_path):
    """
    Gets the URLs of the cached styles.
    """
    try:
        cached_styles = os.listdir(cache_path)
    except IOError as ex:
        if ex.errno != errno.ENOENT and ex.errno != errno.ESRCH:
            raise
        return []
    except OSError:
        return []
    return [url_for('render_cache', filename=style)
            for style in cached_styles
            if style.endswith('.css')]


def _find_file(path, force=False):
    """
    Gets the full path and extension.
    """
    if path is None:
        path = '.'
    for filename in default_filenames:
        full_path = os.path.join(path, filename) if path else filename
        if os.path.exists(full_path):
            return full_path
    if force:
        return os.path.join(path, default_filenames[0])
    raise ValueError('No README found at ' + path)


def _find_file_or_404(path, force):
    """
    Gets the full path and extension, or raises 404.
    """
    try:
        return _find_file(path, force)
    except ValueError:
        abort(404)


def _read_file_or_404(filename, read_as_text=True):
    """
    Reads the contents of the specified file, or raise 404.
    """
    mode = 'rt' if read_as_text else 'rb'
    encoding = 'utf-8' if read_as_text else None
    try:
        with io.open(filename, mode, encoding=encoding) as f:
            return f.read()
    except IOError as ex:
        if ex.errno != errno.ENOENT:
            raise
        abort(404)


def _write_file(filename, contents):
    """
    Creates the specified file and writes the given contents to it.
    """
    write_path = os.path.dirname(filename)
    if not os.path.exists(write_path):
        os.makedirs(write_path)
    with open(filename, 'wb') as f:
        f.write(contents.encode('utf-8'))


def _cache_contents(style_urls, asset_pattern, asset_pattern_sub, cache_path):
    """
    Fetches the given URLs and caches their contents
    and their assets in the given directory.
    """
    files = {}

    asset_urls = []
    for style_url in style_urls:
        print(' * Downloading style', style_url, file=sys.stderr)
        filename = _cache_filename(style_url, cache_path)
        r = requests.get(style_url)
        if not 200 <= r.status_code < 300:
            print(' -> Warning: Style request responded with', r.status_code,
                  file=sys.stderr)
            files = None
            continue
        contents = r.text
        # Find assets and replace their base URLs with the cache directory
        asset_urls += map(lambda url: urljoin(style_url, url),
                          re.findall(asset_pattern, contents))
        contents = re.sub(asset_pattern, asset_pattern_sub, contents)
        # Prepare cache
        if files:
            files[filename] = contents

    for asset_url in asset_urls:
        print(' * Downloading asset', asset_url, file=sys.stderr)
        filename = _cache_filename(asset_url, cache_path)
        # Retrieve file and show message
        r = requests.get(asset_url)
        if not 200 <= r.status_code < 300:
            print(' -> Warning: Asset request responded with', r.status_code,
                  file=sys.stderr)
            files = None
            continue
        # Prepare cache
        if files:
            files[filename] = r.text

    # Skip caching if something went wrong to try again next time
    if not files:
        return False

    # Cache files if all downloads were successful
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    for filename in files:
        _write_file(filename, files[filename])

    print(' * Cached all downloads in', cache_path, file=sys.stderr)
    return True


def _normalize_url(url):
    return url.rsplit('?', 1)[0].rsplit('#', 1)[0]


def _cache_filename(url, cache_path):
    basename = _normalize_url(url).rsplit('/', 1)[-1]
    filename = os.path.join(cache_path, basename)
    return filename
