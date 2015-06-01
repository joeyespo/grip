from __future__ import print_function

import io
import os
import sys
import errno

from .server import create_app, resolve_readme
from .renderer import render_app


def render_page(path=None, gfm=False, context=None,
                username=None, password=None,
                render_offline=False, render_wide=False, render_inline=False,
                text=None, api_url=None, title=None):
    """
    Renders the specified markup text to an HTML page and returns it.
    """
    app = create_app(path, gfm, context, username, password, render_offline,
                     render_wide, render_inline, text, api_url, title)
    return render_app(app)


def export(path=None, gfm=False, context=None, username=None, password=None,
           render_offline=False, render_wide=False, render_inline=True,
           out_filename=None, api_url=None, title=None):
    """
    Exports the rendered HTML to a file.
    """
    export_to_stdout = out_filename == '-'
    if out_filename is None:
        if path == '-':
            export_to_stdout = True
        else:
            out_filename = os.path.splitext(resolve_readme(path))[0] + '.html'

    if not export_to_stdout:
        print('Exporting to', out_filename, file=sys.stderr)

    page = render_page(path, gfm, context, username, password, render_offline,
                       render_wide, render_inline, None, api_url, title)

    if export_to_stdout:
        try:
            print(page)
        except IOError as ex:
            if ex.errno != 0 and ex.errno != errno.EPIPE:
                raise
    else:
        with io.open(out_filename, 'w', encoding='utf-8') as f:
            f.write(page)
