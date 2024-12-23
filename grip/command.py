"""\
grip.command
~~~~~~~~~~~~

Implements the command-line interface for Grip.


Usage:
  grip [options] [<path>] [<address>]
  grip -V | --version
  grip -h | --help

Where:
  <path> is a file to render or a directory containing README.md (- for stdin)
  <address> is what to listen on, of the form <host>[:<port>], or just <port>

Options:
  --user-content    Render as user-content like comments or issues.
  --context=<repo>  The repository context, only taken into account
                    when using --user-content.
  --user=<username> A GitHub username for API authentication. If used
                    without the --pass option, an upcoming password
                    input will be necessary.
  --pass=<password> A GitHub password or auth token for API auth.
  --wide            Renders wide, i.e. when the side nav is collapsed.
                    This only takes effect when --user-content is used.
  --clear           Clears the cached styles and assets and exits.
  --export          Exports to <path>.html or README.md instead of
                    serving, optionally using [<address>] as the out
                    file (- for stdout).
  --no-inline       Link to styles instead inlining when using --export.
  -b --browser      Open a tab in the browser after the server starts.
  --api-url=<url>   Specify a different base URL for the github API,
                    for example that of a Github Enterprise instance.
                    Default is the public API: https://api.github.com
  --title=<title>   Manually sets the page's title.
                    The default is the filename.
  --norefresh       Do not automatically refresh the Readme content when
                    the file changes.
  --quiet           Do not print to the terminal.
  --theme=<theme>   Theme to view markdown file (light mode or dark mode).
                    Default: "auto" Valid options: (as of writing)
                        - `auto` -- defaults to `light`
                        - `light`
                        - `dark`
                        - `dark_colorblind`
                        - `dark_dimmed`
                        - `dark_high_contrast`
                        - `dark_tritanopia`
                        - `light_colorblind`
                        - `light_high_contrast`
                        - `light_tritanopia`
"""

from __future__ import annotations
from __future__ import print_function

import errno
import mimetypes
import socket
import sys
from getpass import getpass

from docopt import docopt
from path_and_address import resolve
from path_and_address import split_address

from . import __version__
from .api import clear_cache
from .api import export
from .api import serve
from .exceptions import ReadmeNotFoundError

usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
version = 'Grip ' + __version__

# Note: GitHub supports more than light mode and dark mode (exp: light-high-constrast, dark-high-constrast).
VALID_THEME_PREFIXES = ['auto', 'light', 'dark']


def main(argv=None, force_utf8=True, patch_svg=True):
    """
    The entry point of the application.
    """
    if force_utf8 and sys.version_info[0] == 2:
        reload(sys)  # noqa
        sys.setdefaultencoding('utf-8')
    if patch_svg and sys.version_info[0] == 2 and sys.version_info[1] <= 6:
        mimetypes.add_type('image/svg+xml', '.svg')

    if argv is None:
        argv = sys.argv[1:]

    # Show specific errors
    if '-a' in argv or '--address' in argv:
        print('Use grip [options] <path> <address> instead of -a')
        print('See grip -h for details')
        return 2
    if '-p' in argv or '--port' in argv:
        print('Use grip [options] [<path>] [<hostname>:]<port> instead of -p')
        print('See grip -h for details')
        return 2

    # Parse options
    args = docopt(usage, argv=argv, version=version)

    # Handle printing version with -V (docopt handles --version)
    if args['-V']:
        print(version)
        return 0

    # Clear the cache
    if args['--clear']:
        clear_cache()
        return 0

    # Get password from prompt if necessary
    password = args['--pass']
    if args['--user'] and not password:
        password = getpass()

    # Parse theme argument
    theme: str | None = args["--theme"]
    if theme:
        for prefix in VALID_THEME_PREFIXES:
            if theme.startswith(prefix):
                break
        else:
            print('Error: invalid value for theme: %r', theme)
            return 1

    # Export to a file instead of running a server
    if args['--export']:
        try:
            export(args['<path>'], args['--user-content'], args['--context'],
                   args['--user'], password, False, args['--wide'],
                   not args['--no-inline'], args['<address>'],
                   args['--api-url'], args['--title'], args['--quiet'], theme)
            return 0
        except ReadmeNotFoundError as ex:
            print('Error:', ex)
            return 1

    # Parse arguments
    path, address = resolve(args['<path>'], args['<address>'])
    host, port = split_address(address)

    # Validate address
    if address and not host and port is None:
        print('Error: Invalid address', repr(address))

    # Run server
    try:
        serve(path, host, port, args['--user-content'], args['--context'],
              args['--user'], password, False, args['--wide'], False,
              args['--api-url'], args['--title'], not args['--norefresh'],
              args['--browser'], args['--quiet'], theme, None)
        return 0
    except ReadmeNotFoundError as ex:
        print('Error:', ex)
        return 1
    except socket.error as ex:
        print('Error:', ex)
        if ex.errno == errno.EADDRINUSE:
            print('This port is in use. Is a grip server already running? '
                  'Stop that instance or specify another port here.')
        return 1
