import os
import settings
from urllib2 import urlopen
from server import _get_style_urls, _find_file, _read_file
from renderer import render_page


config_vars = [var for var in dir(settings) if not var.startswith('__')]
config = {var: getattr(settings, var) for var in config_vars}
try:
    import settings_local
    config_vars = [var for var in dir(settings_local) if not var.startswith('__')]
    config.update({var: getattr(settings_local, var) for var in config_vars})
except ImportError:
    pass


def write_html(path=None):
    """Exports the rendered HTML to a file."""
    style_urls = _get_style_urls(config['STYLE_URL_SOURCE'], config['STYLE_URL_RE'])
    style_url_contents = [urlopen(css).read().decode('utf-8') for css in style_urls]

    if not path or os.path.isdir(path):
        fname_in = _find_file(path)
        text = _read_file(fname_in)
        outname = os.path.splitext(fname_in)[0] + '.html'
    else:
        text = _read_file(path)
        outname = os.path.splitext(path)[0] + '.html'
    page = render_page(text=text, style_url_contents=style_url_contents)

    with open(outname, 'w') as f:
        f.write(page.encode('utf-8'))
