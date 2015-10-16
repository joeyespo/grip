from __future__ import print_function

import io
import os
import sys
import errno

from .server import create_app, resolve_readme
from .renderer import render_app


def render_page(path=None, user_content=False, context=None,
                username=None, password=None,
                render_offline=False, render_wide=False, render_inline=False,
                api_url=None, title=None, text=None):
    """
    Renders the specified markup text to an HTML page and returns it.
    """
    app = create_app(path, user_content, context, username, password,
                     render_offline, render_wide, render_inline, api_url,
                     title, text, False, None)
    return render_app(app)


def export(path=None, user_content=False, context=None, username=None,
           password=None, render_offline=False, render_wide=False,
           render_inline=True, out_filename=None, api_url=None, title=None):
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

    page = render_page(path, user_content, context, username, password,
                       render_offline, render_wide, render_inline, api_url,
                       title, None)

    if export_to_stdout:
        try:
            print(page)
        except IOError as ex:
            if ex.errno != 0 and ex.errno != errno.EPIPE:
                raise
    else:
        with io.open(out_filename, 'w', encoding='utf-8') as f:
            f.write(page)
