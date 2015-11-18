"""\
Default Configuration

Do NOT change the values here for risk of accidentally committing them.
Override them using command-line arguments or with a settings_local.py in
this directory or in ~/.grip/settings.py instead.
"""


HOST = 'localhost'
PORT = 6419
DEBUG = False
DEBUG_GRIP = False
CACHE_DIRECTORY = 'cache-{version}'
AUTOREFRESH = True
QUIET = False


# Note: For security concerns, please don't save your GitHub password in your
# local settings.py. Use a personal access token instead:
# https://github.com/settings/tokens/new?scopes=
USERNAME = None
PASSWORD = None


# Custom GitHub API
API_URL = None


# Custom styles
STYLE_URLS = []
