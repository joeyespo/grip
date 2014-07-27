from __future__ import print_function

import io
import os
from .server import create_app, resolve_readme
from .renderer import render_app


def render_page(path=None, gfm=False, context=None,
                username=None, password=None,
                render_offline=False, render_wide=False, render_inline=False,
                text=None):
    """Renders the specified markup text to an HTML page and returns it."""
    app = create_app(path, gfm, context, username, password,
                     render_offline, render_wide, render_inline, text)
    return render_app(app)


def export(path=None, gfm=False, context=None, username=None, password=None,
           render_offline=False, render_wide=False, render_inline=True,
           out_filename=None):
    """Exports the rendered HTML to a file."""
    if out_filename is None:
        out_filename = os.path.splitext(resolve_readme(path))[0] + '.html'

    print('Exporting to', out_filename)

    page = render_page(path, gfm, context, username, password,
                          render_offline, render_wide, render_inline)
    with io.open(out_filename, 'w', encoding='utf-8') as f:
        f.write(page)
