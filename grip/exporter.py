import default_config as dc
import os
from server import _get_styles
from urllib2 import urlopen
from renderer import render_page
from server import _find_file, _read_file
from flask import safe_join

vars_dc = [var for var in dir(dc) if not var.startswith('__')]
settings = {var: getattr(dc, var) for var in vars_dc}
try:
    import config as cc
    vars_cc = [var for var in dir(cc) if not var.startswith('__')]
    settings.update({var: getattr(cc, var) for var in vars_cc})
except ImportError:
    pass
''' Exports readme files to a monolithic HTML '''

def write_html(path=None):
    """Exports a Html file 
    
    Arguments:
    - `type`:
    - `fname`:
    """
    style_urls = _get_styles(settings['STYLE_URL_SOURCE'],
                             settings['STYLE_URL_RE'])
    
    style_url_contents = [urlopen(css).read().decode('utf-8')
                          for css in style_urls]

    if not path or os.path.isdir(path):
        fname_in = _find_file(path)
        text = _read_file(fname_in)
        outname = os.path.splitext(fname_in)[0]+".html"
    else:
        text = _read_file(path)
        outname = os.path.splitext(path)[0]+".html"
    page = render_page(text=text,style_url_contents=style_url_contents)

    with open(outname, "w") as f:
        f.write(page.encode('utf-8'))

