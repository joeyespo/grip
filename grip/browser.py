import socket
import time
import webbrowser
from threading import Thread


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


def wait_and_start_browser(host, port=None, cancel_event=None):
    """
    Waits for the server to run and then opens the specified address in
    the browser. Set cancel_event to cancel the wait.
    """
    if host == '0.0.0.0':
        host = 'localhost'
    if port is None:
        port = 80

    if wait_for_server(host, port, cancel_event):
        start_browser('http://{0}:{1}/'.format(host, port))


def start_browser_when_ready(host, port=None, cancel_event=None):
    """
    Starts a thread that waits for the server then opens the specified
    address in the browser. Set cancel_event to cancel the wait. The
    started thread object is returned.
    """
    browser_thread = Thread(
        target=wait_and_start_browser, args=(host, port, cancel_event))
    browser_thread.daemon = True
    browser_thread.start()
    return browser_thread
