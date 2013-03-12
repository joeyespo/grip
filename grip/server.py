import os
import re
import requests
from flask import Flask, safe_join, abort
from .renderer import render_page


default_filenames = ['README.md', 'README.markdown']


def serve(path=None, host=None, port=None, gfm=False, context=None):
    """Starts a server to render the specified file or directory containing a README."""
    if not path or os.path.isdir(path):
        index_file, path = _find_index_file(path)

    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)

    # Flask application
    app = Flask('grip')
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('local_config.py', silent=True)

    # Get styles from style source
    @app.before_first_request
    def retrieve_styles():
        if not app.config['STYLE_URL_SOURCE'] or not app.config['STYLE_URL_RE']:
            return
        styles = _get_styles(app.config['STYLE_URL_SOURCE'], app.config['STYLE_URL_RE'])
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
    def index():
        return render_page(_read_file(index_file), os.path.split(index_file)[1], gfm, context, app.config['STYLE_URLS'])

    @app.route('/<path:filename>')
    def other_files(filename):
        try:
            full_file = safe_join(path, filename)
            return render_page(_read_file(full_file), os.path.split(filename)[1], gfm, context, app.config['STYLE_URLS'])
        except:
            abort(404)

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.debug, use_reloader=app.config['DEBUG_GRIP'])


def _get_styles(source_url, pattern):
    """Gets the specified resource and parses all styles in the form of the specified pattern."""
    try:
        r = requests.get(source_url)
        if not 200 <= r.status_code < 300:
            print ' * Warning: retrieving styles gave status code', r.status_code
        return re.findall(pattern, r.text)
    except Exception, e:
        print ' * Error: could not retrieve styles:', str(e)
        return []


def _find_index_file(path):
    """Finds the index file. Returns the index file and root path."""
    if path is None:
        path = '.'
    for filename in default_filenames:
        index_file = os.path.join(path, filename)
        if os.path.exists(index_file):
            return index_file, path
    raise ValueError('No README found at ' + path)


def _read_file(filename):
    """Reads the contents of the specified file."""
    with open(filename) as f:
        return f.read()
