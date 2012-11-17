from flask import Flask
from .renderer import render_page
from .watcher import find_readme, read_file


def serve(directory='.', readme_file='README'):
    """Starts a server to render the readme from the specified directory."""

    # Get the README filename
    filename = find_readme(directory, readme_file)
    if not filename:
        raise ValueError('No %s file found at %s' % ('README' if readme_file == 'README' else repr(readme_file), repr(directory)))

    # Flask application
    app = Flask('grip')
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('local_config.py', silent=True)

    # Views
    @app.route('/')
    def index():
        return render_page(read_file(filename), filename)

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=True, use_reloader=app.config['DEBUG_GRIP'])
