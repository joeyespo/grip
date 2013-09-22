import io
import os
from server import create_app


def export(path=None, gfm=False, context=None, username=None, password=None,
           render_offline=False,):
    """Exports the rendered HTML to a file."""
    app = create_app(path, gfm, context, username, password, render_offline,
                     render_inline=True)
    out_filename = os.path.splitext(app.config['GRIP_FILE'])[0] + '.html'

    print 'Exporting to', out_filename

    # Render the file
    with app.test_client() as c:
        response = c.get('/')
        encoding = response.charset
        content = response.data.decode(encoding)

    # Save content
    with io.open(out_filename, 'w', encoding=encoding) as f:
        f.write(content)
