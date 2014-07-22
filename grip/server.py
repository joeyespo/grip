from __future__ import print_function

import os
import re
import errno
import shutil
import base64
import mimetypes
import requests
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
from traceback import format_exc
from flask import Flask, safe_join, abort, url_for, send_from_directory
from .constants import default_filenames
from .renderer import render_page, render_image


def create_app(path=None, gfm=False, context=None,
               username=None, password=None,
               render_offline=False, render_wide=False, render_inline=False):
    """
    Creates an WSGI application that can serve the specified file or
    directory containing a README.
    """
    in_filename = resolve_readme(path)

    # Create Flask application
    app = _create_flask()

    # Runtime config
    username = username if username is not None else app.config.get('USERNAME')
    password = password if password is not None else app.config.get('PASSWORD')

    # Authentication message
    if username:
        print(' * Using credentials:', username)

    # Setup style cache
    if app.config['CACHE_DIRECTORY']:
        cache_path = os.path.join(app.instance_path,
                                  app.config['CACHE_DIRECTORY'])
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
    else:
        cache_path = None
    cache_url = app.config.get('CACHE_URL')

    # Get initial styles
    style_urls = list(app.config['STYLE_URLS'] or [])
    styles = []

    # Get styles from style source
    @app.before_first_request
    def retrieve_styles():
        """Retrieves the style URLs from the source and caches them."""
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
                filename = _find_file_or_404(filename)
            # Read and serve images as binary
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype and mimetype.startswith('image/'):
                text = _read_file_or_404(filename, True)
                return render_image(text, mimetype)
        else:
            filename = in_filename

        text = _read_file_or_404(filename)
        return render_page(text, filename, gfm, context,
                           username, password, render_offline,
                           style_urls, styles,
                           None, render_wide)

    @app.route(cache_url + '/<path:filename>')
    def render_cache(filename=None):
        return send_from_directory(cache_path, filename)

    return app


def serve(path=None, host=None, port=None, gfm=False, context=None,
          username=None, password=None,
          render_offline=False, render_wide=False):
    """
    Starts a server to render the specified file
    or directory containing a README.
    """
    app = create_app(path, gfm, context, username, password,
                     render_offline, render_wide, False)

    # Set overridden config values
    if host is not None:
        app.config['HOST'] = host
    if port is not None:
        app.config['PORT'] = port

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.debug,
        use_reloader=app.config['DEBUG_GRIP'])


def clear_cache():
    """Clears the cached styles and assets."""
    app = _create_flask()
    cache_path = os.path.join(app.instance_path, app.config['CACHE_DIRECTORY'])
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    print('Cache cleared.')


def resolve_readme(path=None):
    """
    Returns the path if it's a file; otherwise, looks for a compatible README
    file in the directory specified by path. If path is None, the current
    working directory is used. If no compatible README can be found,
    a ValueError is raised.
    """
    if not path or os.path.isdir(path):
        path = _find_file(path)
    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)
    return os.path.normpath(path)


def _create_flask():
    instance_path = os.path.abspath(os.path.expanduser('~/.grip'))
    user_settings = os.path.join(instance_path, 'settings.py')

    # Flask application
    app = Flask(__name__, instance_path=instance_path)
    app.config.from_object('grip.settings')
    app.config.from_pyfile('settings_local.py', silent=True)
    app.config.from_pyfile(user_settings, silent=True)

    return app


def _get_style_urls(source_url, style_pattern, asset_pattern,
                    asset_pattern_sub, cache_path, debug=False):
    """
    Gets the specified resource and parses all style URLs and their assets
    in the form of the specified patterns.
    """
    try:
        # Skip fetching styles if there's any already cached
        if cache_path:
            cached = _get_cached_style_urls(cache_path)
            if cached:
                return cached

        # Find style URLs
        r = requests.get(source_url)
        if not 200 <= r.status_code < 300:
            print(' * Warning: retrieving styles gave status code',
                  r.status_code)
        urls = re.findall(style_pattern, r.text)

        # Cache the styles and their assets
        if cache_path:
            _cache_contents(urls, asset_pattern, asset_pattern_sub, cache_path)
            urls = _get_cached_style_urls(cache_path)

        return urls
    except Exception as ex:
        if debug:
            print(format_exc())
        else:
            print(' * Error: could not retrieve styles:', ex)
        return []


def _get_styles(app, style_urls, asset_pattern):
    """Gets the content of the given list of style URLs and inlines assets."""
    styles = []
    for style_url in style_urls:

        def match_asset(match):
            url = urljoin(style_url, _normalize_url(match.group(1)))
            ext = os.path.splitext(url)[1][1:]
            asset = _download(app, url)
            asset64 = base64.b64encode(asset)
            data_url = 'url(data:font/{0};base64,{1})'.format(ext, asset64)
            return data_url

        content = re.sub(asset_pattern, match_asset, _download(app, style_url))
        styles.append(content)

    return styles


def _download(app, url):
    if urlparse(url).netloc:
        return requests.get(url).content

    with app.test_client() as c:
        return c.get(url).data


def _get_cached_style_urls(cache_path):
    """Gets the URLs of the cached styles."""
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


def _find_file(path):
    """Gets the full path and extension of the specified."""
    if path is None:
        path = '.'
    for filename in default_filenames:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    raise ValueError('No README found at ' + path)


def _find_file_or_404(path):
    """Gets the full path and extension of the specified, or raises 404."""
    try:
        return _find_file(path)
    except ValueError:
        abort(404)


def _read_file_or_404(filename, read_as_binary=False):
    """Reads the contents of the specified file, or raise 404."""
    mode = 'rb' if read_as_binary else 'r'
    try:
        with open(filename, mode) as f:
            return f.read()
    except IOError as ex:
        if ex.errno != errno.ENOENT:
            raise
        abort(404)


def _write_file(filename, contents):
    """Creates the specified file and writes the given contents to it."""
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
    asset_urls = []
    for style_url in style_urls:
        filename = _cache_filename(style_url, cache_path)
        contents = requests.get(style_url).text
        # Find assets and replace their base URLs with the cache directory
        asset_urls += map(lambda url: urljoin(style_url, url),
                          re.findall(asset_pattern, contents))
        contents = re.sub(asset_pattern, asset_pattern_sub, contents)
        # Write file and show message
        _write_file(filename, contents)
        print(' * Cached', style_url, 'in', cache_path)

    for asset_url in asset_urls:
        filename = _cache_filename(asset_url, cache_path)
        contents = requests.get(asset_url).text
        # Write file and show message
        _write_file(filename, contents)
        print(' * Cached', asset_url, 'in', cache_path)


def _normalize_url(url):
    return url.rsplit('?', 1)[0].rsplit('#', 1)[0]


def _cache_filename(url, cache_path):
    basename = _normalize_url(url).rsplit('/', 1)[-1]
    filename = os.path.join(cache_path, basename)
    return filename
