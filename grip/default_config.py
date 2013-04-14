"""\
Default Configuration

Do NOT change the values here for risk of accidentally committing them.
Override them using command-line arguments or with a local_config.py instead.
"""
import os

HOST = 'localhost'
PORT = 5000
DEBUG = True

DEBUG_GRIP = False
STYLE_URLS = []
STYLE_URL_SOURCE = 'https://github.com/joeyespo/grip'
STYLE_URL_RE = '<link.+href=[\'"]?([^\'" >]+)[\'"]?.+media=[\'"]?(?:screen|all)[\'"]?.+rel=[\'"]?stylesheet[\'"]?.+/>'

STYLE_CACHE = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(STYLE_CACHE):
    os.mkdir(STYLE_CACHE)
