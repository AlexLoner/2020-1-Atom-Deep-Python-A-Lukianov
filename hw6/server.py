import socket
import sys
import requests
from help_func import get_data, send_data
from http_helpers import HttpParser

if __name__ == '__main__':
    n = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 5013))
    server.listen(1)
    for i in range(n):
        conn, addr = server.accept()

        data = get_data(conn)
        url = data.decode('utf-8')
        if not url.startswith('http://') or not url.startswith('https://'):
            url = f'https://{url}'
        req = requests.get(url=url)
        obj = HttpParser(reqst=req)
        js_obj = obj.top10()
        send_data(conn, js_obj)
        conn.close()
    server.close()
