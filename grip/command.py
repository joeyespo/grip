"""\
grip.command
~~~~~~~~~~~~

Implements the command-line interface for Grip.


Usage:
  grip [options] [<path>] [<address>]
  grip -h | --help
  grip --version

Where:
  <path> is the path to the working directory of a content repository
  <address> is what to listen on, of the form <host>[:<port>], or just <port>
"""

import os
import sys
import re
from docopt import docopt
from .server import serve
from . import __version__


usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])


def main(initial_args=None):
    """The entry point of the application."""
    if initial_args is None:
        initial_args = sys.argv[1:]
    version = 'Grip ' + __version__

    # Parse options
    args = docopt(usage, argv=initial_args, version=version)

    # Parse arguments
    path, address = _resolve_path(args['<path>'], args['<address>'])
    directory, filename = _split_path(path)
    host, port = _split_address(address)

    # Validate address
    if address and not host and not port:
        print 'Error: Invalid address', repr(address)

    # Run server
    try:
        serve(directory, filename, host, port)
    except ValueError, ex:
        print 'Error:', ex
        return 1

    return 0


def _resolve_path(path_or_address, address=None):
    """Returns (path, address) based on consecutive optional arguments, [path] [address]."""

    if path_or_address is None or address is not None:
        return path_or_address, address

    path = None
    if not _valid_address(path_or_address) or os.path.exists(path_or_address):
        path = path_or_address
    else:
        address = path_or_address

    return path, address


def _split_path(path):
    """Returns (directory, filename) from the specified path."""
    if path is None:
        return None, None

    if path.endswith('.'):
        path += os.path.sep

    directory, filename = os.path.split(path)

    if filename == '':
        filename = None

    return directory, filename


def _split_address(address):
    """Returns (host, port) from the specified address string."""
    invalid = None, None
    if not address:
        return invalid

    components = address.split(':')
    
    if len(components) > 2 or not _valid_hostname(components[0]):
        return invalid

    if len(components) == 2 and not _valid_port(components[1]):
        return invalid

    if len(components) == 1:
        components.insert(0 if _valid_port(components[0]) else 1, None)

    host, port = components
    port = int(port) if port else None

    return host, port


def _valid_address(address):
    """Determines whether the specified address string is valid."""
    if not address:
        return False

    components = address.split(':')
    if len(components) > 2 or not _valid_hostname(components[0]):
        return False

    if len(components) == 2 and not _valid_port(components[1]):
        return False

    return True


def _valid_hostname(host):
    """Returns whether the specified string is a valid hostname."""
    if len(host) > 255:
        return False
    if host[-1:] == '.':
        host = host[:-1]
    allowed = re.compile('(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)
    return all(allowed.match(x) for x in host.split('.'))


def _valid_port(port):
    """Returns whether the specified string is a valid port."""
    try:
        return 1 <= int(port) <= 65535
    except:
        return False
