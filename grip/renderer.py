from .config import STYLE_URLS
from jinja2 import Environment, PackageLoader
import requests


env = Environment(loader=PackageLoader('grip', 'templates'))
index_template = env.get_template('index.html')


def render_content(text):
    """Renders the specified markup."""
    headers = {'content-type': 'text/plain'}
    r = requests.post('https://api.github.com/markdown/raw', headers=headers, data=text)
    return r.text


def render_page(text, filename=None):
    """Renders the specified markup text to an HTML page."""
    return index_template.render(content=render_content(text), filename=filename, style_urls=STYLE_URLS)
