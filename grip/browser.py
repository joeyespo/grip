import socket
import webbrowser


def is_server_running(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return not sock.connect_ex((host, port)) == 0


def start_browser(host, port):
    # Waiting for server to start
    while not is_server_running(host, port):
        pass
    try:
        browser_url = "http://{0}:{1}".format(host, port)
        webbrowser.open(browser_url)
    except:
        pass
