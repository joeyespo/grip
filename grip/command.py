"""\
grip.command
~~~~~~~~~~~~

Implements the command-line interface for Grip.


Usage:
  grip [options] [<path>] [<address>]
  grip -h | --help
  grip --version

Where:
  <path> is a file to render or a directory containing a README.md file
  <address> is what to listen on, of the form <host>[:<port>], or just <port>

Options:
  --gfm             Use GitHub-Flavored Markdown, e.g. comments or issues
  --context=<repo>  The repository context, only taken into account with --gfm
  --render-offline  Render offline instead of via GitHub markdown API
  --user=<username> A GitHub username for API authentication
  --pass=<password> A GitHub password for API authentication
  --export          Exports to a given <path>.html if path is a filename, or README.html
                    otherwise
"""

import sys
from path_and_address import resolve, split_address
from docopt import docopt
from .server import serve
from .exporter import write_html
from . import __version__


usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])


def main(argv=None):
    """The entry point of the application."""
    if argv is None:
        argv = sys.argv[1:]
    version = 'Grip ' + __version__

    # Parse options
    args = docopt(usage, argv=argv, version=version)

    # Parse arguments
    path, address = resolve(args['<path>'], args['<address>'])
    host, port = split_address(address)

    # Export to a file instead of running a server
    if args['--export']:
        try:
            write_html(path)
            return 0
        except Exception as e:
            print 'Error:', e
            return 1

    # Validate address
    if address and not host and not port:
        print 'Error: Invalid address', repr(address)

    # Run server
    try:
        serve(path, host, port, args['--gfm'], args['--context'],
              args['--render-offline'], args['--user'], args['--pass'])
        return 0
    except ValueError, ex:
        print 'Error:', ex
        return 1
