import socket
import webbrowser


def start_browser(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #waiting for server to start
    while sock.connect_ex((host, port)) not in [0, 22]:
        pass
    try:
        browser_url = "http://{0}:{1}".format(host, port)
        webbrowser.open(browser_url)
    except:
        pass
