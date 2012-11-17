from .server import serve


def main():
    """The entry point of the command-line interface."""

    # TODO: process arguments

    try:
        serve()
    except ValueError, ex:
        # Show input error
        print 'Error:', ex
