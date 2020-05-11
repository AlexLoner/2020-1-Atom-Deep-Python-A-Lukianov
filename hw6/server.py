import socket
import sys

import requests

# from help_func import get_data
from http_helpers import HttpParser

if __name__ == '__main__':
    n = int(sys.argv[1])
    server = socket.socket()
    server.bind(('', 40404))
    server.listen(1)
    for i in range(n):
        conn, addr = server.accept()
        total_data = []
        while True:
            data = conn.recv(2048)
            if not data:
                break
            total_data.extend([data.decode()])
            url = ''.join(total_data)
            if not url.startswith('http://') or not url.startswith('https://'):
                url = f'https://{url}'
            req = requests.get(url=url)
            obj = HttpParser(reqst=req)
            conn.send(obj.top10().encode())
    conn.close()
