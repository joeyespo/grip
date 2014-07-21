"""\
Default Configuration

Do NOT change the values here for risk of accidentally committing them.
Override them using command-line arguments or with a settings_local.py in
this directory or in ~/.grip/settings.py instead.
"""

HOST = 'localhost'
PORT = 5000
DEBUG = True


DEBUG_GRIP = False


USERNAME = None
PASSWORD = None


STYLE_URLS = []
STYLE_URLS_SOURCE = 'https://github.com/joeyespo/grip'
STYLE_URLS_RE = '<link.+href=[\'"]?([^\'" >]+)[\'"]?.+media=[\'"]?(?:screen|all)[\'"]?.+rel=[\'"]?stylesheet[\'"]?.+/>'
STYLE_CACHE_DIRECTORY = 'style-cache'
