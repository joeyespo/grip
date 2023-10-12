from __future__ import print_function, unicode_literals

import io
import os
import sys
import errno

from .app import Grip
from .readers import DirectoryReader, StdinReader, TextReader
from .renderers import GitHubRenderer, GitLabRenderer, OfflineRenderer


def create_app(path=None, user_content=False, context=None, username=None,
               password=None, render_backend='github', render_wide=False,
               render_inline=False, api_url=None, title=None, text=None,
               autorefresh=None, quiet=None, grip_class=None):
    """
    Creates a Grip application with the specified overrides.
    """
    # Customize the app
    if grip_class is None:
        grip_class = Grip

    # Customize the reader
    if text is not None:
        display_filename = DirectoryReader(path, True).filename_for(None)
        source = TextReader(text, display_filename)
    elif path == '-':
        source = StdinReader()
    else:
        source = DirectoryReader(path)

    # Customize the renderer
    if render_backend == 'github':
        renderer = GitHubRenderer(user_content, context, api_url)
    elif render_backend == 'gitlab':
        renderer = GitLabRenderer(user_content, context, api_url)
    elif render_backend == 'offline':
        renderer = OfflineRenderer(user_content, context)
    else:
        renderer = None

    # Optional basic auth
    auth = (username, password) if username or password else None

    # Create the customized app with default asset manager
    return grip_class(source, auth, renderer, None, render_wide,
                      render_inline, title, autorefresh, quiet)


def serve(path=None, host=None, port=None, user_content=False, context=None,
          username=None, password=None, render_backend='github',
          render_wide=False, render_inline=False, api_url=None, title=None,
          autorefresh=True, browser=False, quiet=None, grip_class=None):
    """
    Starts a server to render the specified file or directory containing
    a README.
    """
    app = create_app(path, user_content, context, username, password,
                     render_backend, render_wide, render_inline, api_url,
                     title, None, autorefresh, quiet, grip_class)
    app.run(host, port, open_browser=browser)


def clear_cache(grip_class=None):
    """
    Clears the cached styles and assets.
    """
    if grip_class is None:
        grip_class = Grip
    grip_class(StdinReader()).clear_cache()


def render_page(path=None, user_content=False, context=None,
                username=None, password=None,
                render_backend='github', render_wide=False,
                render_inline=False, api_url=None, title=None, text=None,
                quiet=None, grip_class=None):
    """
    Renders the specified markup text to an HTML page and returns it.
    """
    return create_app(path, user_content, context, username, password,
                      render_backend, render_wide, render_inline, api_url,
                      title, text, False, quiet, grip_class).render()


def render_content(text, user_content=False, context=None, username=None,
                   password=None, render_backend='github', api_url=None):
    """
    Renders the specified markup and returns the result.
    """
    if render_backend == 'github':
        renderer = GitHubRenderer(user_content, context, api_url)
    elif render_backend == 'gitlab':
        renderer = GitLabRenderer(user_content, context, api_url)
    else:
        renderer = OfflineRenderer(user_content, context)
    auth = (username, password) if username or password else None
    return renderer.render(text, auth)


def export(path=None, user_content=False, context=None,
           username=None, password=None, render_backend='github',
           render_wide=False, render_inline=True, out_filename=None,
           api_url=None, title=None, quiet=False, grip_class=None):
    """
    Exports the rendered HTML to a file.
    """
    export_to_stdout = out_filename == '-'
    if out_filename is None:
        if path == '-':
            export_to_stdout = True
        else:
            filetitle, _ = os.path.splitext(
                os.path.relpath(DirectoryReader(path).root_filename))
            out_filename = '{0}.html'.format(filetitle)

    if not export_to_stdout and not quiet:
        print('Exporting to', out_filename, file=sys.stderr)

    page = render_page(path, user_content, context, username, password,
                       render_backend, render_wide, render_inline, api_url,
                       title, None, quiet, grip_class)

    if export_to_stdout:
        try:
            print(page)
        except IOError as ex:
            if ex.errno != 0 and ex.errno != errno.EPIPE:
                raise
    else:
        with io.open(out_filename, 'w', encoding='utf-8') as f:
            f.write(page)
