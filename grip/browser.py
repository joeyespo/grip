import socket
import webbrowser
import time


def is_server_running(host, port):
    """
    Checks whether a server is currently listening on the specified
    host and port.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        return s.connect_ex((host, port)) == 0
    finally:
        s.close()


def wait_for_server(host, port, cancel_event=None):
    """
    Blocks until a local server is listening on the specified
    host and port. Set cancel_event to cancel the wait.

    This is intended to be used in conjunction with running
    the Flask server.
    """
    while not is_server_running(host, port):
        # Stop waiting if shutting down
        if cancel_event and cancel_event.is_set():
            return False
        time.sleep(0.1)
    return True


def start_browser(url):
    """
    Opens the specified URL in a new browser window.
    """
    try:
        webbrowser.open(url)
    except Exception:
        pass


def wait_and_start_browser(host, port, cancel_event):
    """
    Waits for the server to run and then opens the specified address in
    the browser. Set cancel_event to cancel the wait.
    """
    host = 'localhost' if host == '0.0.0.0' else host
    if wait_for_server(host, port, cancel_event):
        start_browser('http://{0}:{1}/'.format(host, port))
