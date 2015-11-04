from __future__ import print_function, unicode_literals

import io
import os
import sys
import errno

from .app import Grip
from .readers import DirectoryReader, StdinReader, TextReader
from .renderers import GitHubRenderer, OfflineRenderer
from .resolver import resolve_readme


def create_app(path=None, user_content=False, context=None, username=None,
               password=None, render_offline=False, render_wide=False,
               render_inline=False, api_url=None, title=None, text=None,
               autorefresh=None, quiet=None, grip_class=None):
    if grip_class is None:
        grip_class = Grip

    # Find the file
    use_stdin = path == '-' and text is None
    if path == '-':
        path = None
    force_resolve = text is not None or use_stdin
    in_filename = resolve_readme(path, force_resolve)

    # Customize the reader
    if use_stdin:
        source = StdinReader(in_filename)
    elif text is not None:
        source = TextReader(in_filename)
    else:
        source = DirectoryReader(in_filename)

    # Customize the renderer
    if render_offline:
        renderer = OfflineRenderer(user_content, context)
    elif user_content or context or api_url:
        renderer = GitHubRenderer(user_content, context, api_url)
    else:
        renderer = None

    auth = (username, password) if username or password else None
    assets = None
    return grip_class(source, auth, renderer, assets, render_wide,
                      render_inline, title, autorefresh, quiet)


def serve(path=None, host=None, port=None, user_content=False, context=None,
          username=None, password=None, render_offline=False,
          render_wide=False, render_inline=False, api_url=None, title=None,
          autorefresh=True, browser=False, quiet=None, grip_class=None):
    """
    Starts a server to render the specified file or directory containing
    a README.
    """
    app = create_app(path, user_content, context, username, password,
                     render_offline, render_wide, render_inline, api_url,
                     title, None, autorefresh, quiet, grip_class)
    app.run(host, port, open_browser=browser)


def clear_cache(grip_class=None):
    """
    Clears the cached styles and assets.
    """
    if grip_class is None:
        grip_class = Grip
    grip_class().clear_cache()


def render_page(path=None, user_content=False, context=None,
                username=None, password=None,
                render_offline=False, render_wide=False, render_inline=False,
                api_url=None, title=None, text=None, grip_class=None):
    """
    Renders the specified markup text to an HTML page and returns it.
    """
    return create_app(path, user_content, context, username, password,
                      render_offline, render_wide, render_inline, api_url,
                      title, text, False, None, grip_class).render()


def render_content(text, user_content=False, context=None, username=None,
                   password=None, render_offline=False, api_url=None):
    """
    Renders the specified markup and returns the result.
    """
    if not render_offline and api_url is None:
        ValueError('Argument api_url is required when not rendering offline.')
    return (offline_render(text, user_content, context)
            if render_offline
            else github_render(text, api_url, user_content, context, username,
                               password))


def export(path=None, user_content=False, context=None, username=None,
           password=None, render_offline=False, render_wide=False,
           render_inline=True, out_filename=None, api_url=None, title=None,
           grip_class=None):
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
                       title, None, grip_class)

    if export_to_stdout:
        try:
            print(page)
        except IOError as ex:
            if ex.errno != 0 and ex.errno != errno.EPIPE:
                raise
    else:
        with io.open(out_filename, 'w', encoding='utf-8') as f:
            f.write(page)
