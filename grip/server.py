import re
import requests
from flask import Flask
from .renderer import render_page
from .watcher import find_readme, read_file


def serve(directory='.', readme_file='README', port=None):
    """Starts a server to render the readme from the specified directory."""

    # Get the README filename
    filename = find_readme(directory, readme_file)
    if not filename:
        raise ValueError('No %s file found at %s' % ('README' if readme_file == 'README' else repr(readme_file), repr(directory)))

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
    if port is not None:
        app.config['PORT'] = port

    # Views
    @app.route('/')
    def index():
        return render_page(read_file(filename), filename, app.config['STYLE_URLS'])

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.config['DEBUG'], use_reloader=app.config['DEBUG_GRIP'])


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
