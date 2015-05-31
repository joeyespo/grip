"""\
Default Configuration

Do NOT change the values here for risk of accidentally committing them.
Override them using command-line arguments or with a settings_local.py in
this directory or in ~/.grip/settings.py instead.
"""


HOST = 'localhost'
PORT = 6419
DEBUG = True


DEBUG_GRIP = False


# Note: For security concerns, please don't save your GitHub password in your
# local settings.py. Use a personal access token instead:
# https://github.com/settings/tokens/new?scopes=
USERNAME = None
PASSWORD = None


API_URL = 'https://api.github.com'
CACHE_DIRECTORY = 'cache-{version}'
CACHE_URL = '/grip-cache'
STATIC_URL_PATH = '/grip-static'
STYLE_URLS = []
STYLE_URLS_SOURCE = 'https://github.com/joeyespo/grip'
STYLE_URLS_RE = '<link.+href=[\'"]?([^\'" >]+)[\'"]?.+media=[\'"]?(?:screen|all)[\'"]?.+rel=[\'"]?stylesheet[\'"]?.+/>'
STYLE_ASSET_URLS_RE = 'url\([\'"]?/assets/([^\'" \)]+)[\'"]?\)'
STYLE_ASSET_URLS_SUB = 'url("{0}/\\1")'.format(CACHE_URL)
STYLE_ASSET_URLS_INLINE = ('url\([\'"]?((?:/assets|{0})/[^\'" \)]+)[\'"]?\)'
    .format(CACHE_URL))
