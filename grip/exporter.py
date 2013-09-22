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


def export(path=None, gfm=False, context=None, render_offline=False,
           username=None, password=None):
    """Exports the rendered HTML to a file."""
    if not path or os.path.isdir(path):
        path = _find_file(path)

    in_filename = os.path.normpath(path)
    out_filename = os.path.splitext(in_filename)[0] + '.html'
    print 'Exporting to', out_filename

    # TODO: Use the style cache
    style_cache_path = None

    # Get styles
    style_urls = config['STYLE_URLS']
    if config['STYLE_URLS_SOURCE'] and config['STYLE_URLS_RE']:
        retrieved_urls = _get_style_urls(config['STYLE_URLS_SOURCE'],
                                         config['STYLE_URLS_RE'],
                                         style_cache_path,
                                         config['DEBUG'])
        style_urls.extend(retrieved_urls)
    styles = [urlopen(url).read().decode('utf-8') for url in style_urls]

    # Render content
    text = _read_file(in_filename)
    content = render_page(text, in_filename, gfm, context, render_offline,
                          username, password, styles=styles)

    with open(out_filename, 'w') as f:
        f.write(content.encode('utf-8'))
