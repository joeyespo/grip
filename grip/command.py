import sys
from .server import serve


def main():
    """The entry point of the command-line interface."""

    # TODO: more advanced argument processing

    # Handle port
    port = None
    if len(sys.argv) > 1:
        port_arg = sys.argv[1]
        try:
            port = int(port_arg[1:] if port_arg.startswith(':') else port_arg)
        except:
            pass

    try:
        serve(port=port)
    except ValueError, ex:
        # Show input error
        print 'Error:', ex
