import os
import re
import errno
import requests
from flask import Flask, safe_join, abort, url_for
from .renderer import render_page


default_filenames = ['README.md', 'README.markdown']


def serve(path=None, host=None, port=None, gfm=False, context=None,
          render_offline=False):
    """Starts a server to render the specified file or directory containing a README."""
    if not path or os.path.isdir(path):
        path = _find_file(path)

    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)

    directory = os.path.dirname(path)

    # Flask application
    app = Flask('grip')
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('local_config.py', silent=True)

    # Get styles from style source
    @app.before_first_request
    def retrieve_styles():
        if not (app.config['STYLE_URL_SOURCE'] and app.config['STYLE_URL_RE'] and app.config['STYLE_CACHE']):
            return

        styles = _get_styles(app.config['STYLE_URL_SOURCE'], app.config['STYLE_URL_RE'],
                             app.config['STYLE_CACHE'])
        app.config['STYLE_URLS'] += styles
        if app.config['DEBUG_GRIP']:
            print ' * Retrieved %s style URL%s' % (len(styles), '' if len(styles) == 1 else 's')

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
                filename = _find_file(filename)
            try:
                text = _read_file(filename)
            except IOError as ex:
                if ex.errno != errno.ENOENT:
                    raise
                return abort(404)
        else:
            text = _read_file(path)
        return render_page(text, filename, gfm, context, render_offline,
                           app.config['STYLE_URLS'])

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.debug, use_reloader=app.config['DEBUG_GRIP'])


def _get_styles(source_url, pattern, cache_dir):
    """Gets the specified resource and parses all styles in the form of the specified pattern."""
    try:
        cached_styles = os.listdir(cache_dir)
        if cached_styles:
            return [url_for('static', filename=style) for style in cached_styles]

        r = requests.get(source_url)
        if not 200 <= r.status_code < 300:
            print ' * Warning: retrieving styles gave status code', r.status_code
        urls = re.findall(pattern, r.text)
        return _cache_contents(urls, cache_dir)
    except Exception, e:
        print ' * Error: could not retrieve styles:', str(e)
        return []


def _find_file(path):
    """Gets the full path and extension of the specified."""
    if path is None:
        path = '.'
    for filename in default_filenames:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    raise ValueError('No README found at ' + path)


def _read_file(filename):
    """Reads the contents of the specified file."""
    with open(filename) as f:
        return f.read()


def _write_file(filename, contents):
    """Creates the specified file and writes the given contents to it."""
    with open(filename, 'w') as f:
        f.write(contents.encode('utf-8'))


def _cache_contents(urls, cache_dir):
    """
    Fetches the given urls and caches their contents in the app's
    static/ directory, so that flask can serve them locally.
    Returns the static file urls.
    """
    static_urls = []
    for url in urls:
        basename = url.rsplit('/', 1)[-1]
        filename = os.path.join(cache_dir, basename)
        contents = requests.get(url).text
        _write_file(filename, contents)
        static_urls.append(url_for('static', filename=basename))
    return static_urls
