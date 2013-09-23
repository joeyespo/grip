import io
import os
from server import create_app
from renderer import render_app


def export(path=None, gfm=False, context=None, username=None, password=None,
           render_offline=False, out_filename=None):
    """Exports the rendered HTML to a file."""
    app = create_app(path, gfm, context, username, password, render_offline,
                     render_inline=True)

    if out_filename is None:
        out_filename = os.path.splitext(app.config['GRIP_FILE'])[0] + '.html'
    print 'Exporting to', out_filename

    content = render_app(app)
    with io.open(out_filename, 'w', encoding='utf-8') as f:
        f.write(content)
