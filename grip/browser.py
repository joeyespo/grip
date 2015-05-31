import socket
import webbrowser


def is_server_running(host, port):
    """
    Checks whether a server is currently listening on the specified
    host and port.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return not sock.connect_ex((host, port)) == 0


def wait_for_server(host, port):
    """
    Blocks until a local server is listening on the specified
    host and port.

    This is intended to be used in conjunction with running
    the Flask server.
    """
    while not is_server_running(host, port):
        pass


def start_browser(url):
    """
    Opens the specified URL in a new browser window.
    """
    try:
        webbrowser.open(url)
    except Exception:
        pass


def wait_and_start_browser(host, port):
    wait_for_server(host, port)
    start_browser('http://{0}:{1}/'.format(host, port))
