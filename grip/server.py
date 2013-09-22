import os
import re
import errno
import requests
import mimetypes
from traceback import format_exc
from flask import Flask, current_app, safe_join, abort, url_for, send_from_directory
from .renderer import render_page, render_image


default_filenames = ['README.md', 'README.markdown']


def serve(path=None, host=None, port=None, gfm=False, context=None,
          render_offline=False, username=None, password=None):
    """Starts a server to render the specified file or directory containing a README."""
    if not path or os.path.isdir(path):
        path = _find_file(path)

    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)

    directory = os.path.dirname(path)

    # Flask application
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.config.from_pyfile('settings_local.py', silent=True)

    # Setup style cache
    style_urls = app.config['STYLE_URLS']
    if app.config['STYLE_CACHE_DIRECTORY']:
        style_cache_path = os.path.join(app.instance_path, app.config['STYLE_CACHE_DIRECTORY'])
        if not os.path.exists(style_cache_path):
            os.makedirs(style_cache_path)
    else:
        style_cache_path = None

    # Get styles from style source
    @app.before_first_request
    def retrieve_styles():
        """Retrieves the style URLs from the source and caches them, if requested."""
        if not app.config['STYLE_URLS_SOURCE'] or not app.config['STYLE_URLS_RE']:
            return

        # Fetch style URLs
        style_urls.extend(
            _get_style_urls(app.config['STYLE_URLS_SOURCE'],
                app.config['STYLE_URLS_RE'], style_cache_path))

    # Set overridden config values
    if host is not None:
        app.config['HOST'] = host
    if port is not None:
        app.config['PORT'] = port

    # Views
    @app.route('/')
    @app.route('/<path:filename>')
    def render(filename=None):
        if filename is not None:
            filename = safe_join(directory, filename)
            if os.path.isdir(filename):
                try:
                    filename = _find_file(filename)
                except ValueError:
                    abort(404)

            # if we think this file is an image, we need to read it in
            # binary mode and serve it as such
            mimetype, _ = mimetypes.guess_type(filename)
            is_image = mimetype.startswith('image/') if mimetype else False

            try:
                text = _read_file(filename, is_image)
            except IOError as ex:
                if ex.errno != errno.ENOENT:
                    raise
                return abort(404)

            if is_image:
                return render_image(text, mimetype)

            filename_display = os.path.normpath(filename)
        else:
            text = _read_file(path)
            filename_display = os.path.normpath(path)
        return render_page(text, filename_display, gfm, context, render_offline,
                           username, password, style_urls)

    @app.route('/cache/<path:filename>')
    def render_cache(filename=None):
        return send_from_directory(style_cache_path, filename)

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.debug,
        use_reloader=app.config['DEBUG_GRIP'])


def _get_style_urls(source_url, pattern, style_cache_path):
    """Gets the specified resource and parses all style URLs in the form of the specified pattern."""
    try:
        # TODO: Add option to clear the cached styles
        # Skip fetching styles if there's any already cached
        if style_cache_path:
            cached = _get_cached_style_urls(style_cache_path)
            if cached:
                return cached

        # Find style URLs
        r = requests.get(source_url)
        if not 200 <= r.status_code < 300:
            print ' * Warning: retrieving styles gave status code', r.status_code
        urls = re.findall(pattern, r.text)

        # Cache the styles
        if style_cache_path:
            _cache_contents(urls, style_cache_path)
            urls = _get_cached_style_urls(style_cache_path)

        return urls
    except Exception as ex:
        if current_app.config['DEBUG_GRIP']:
            print format_exc()
        else:
            print ' * Error: could not retrieve styles:', str(ex)
        return []


def _get_cached_style_urls(style_cache_path):
    """Gets the URLs of the cached styles."""
    cached_styles = os.listdir(style_cache_path)
    return [url_for('render_cache', filename=style) for style in cached_styles]


def _find_file(path):
    """Gets the full path and extension of the specified."""
    if path is None:
        path = '.'
    for filename in default_filenames:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    raise ValueError('No README found at ' + path)


def _read_file(filename, read_as_binary=False):
    """Reads the contents of the specified file."""
    mode = "rb" if read_as_binary else "r"
    with open(filename, mode) as f:
        return f.read()


def _write_file(filename, contents):
    """Creates the specified file and writes the given contents to it."""
    with open(filename, 'w') as f:
        f.write(contents.encode('utf-8'))


def _cache_contents(urls, style_cache_path):
    """Fetches the given URLs and caches their contents in the given directory."""
    for url in urls:
        basename = url.rsplit('/', 1)[-1]
        filename = os.path.join(style_cache_path, basename)
        contents = requests.get(url).text
        _write_file(filename, contents)
        print ' * Downloaded', url
