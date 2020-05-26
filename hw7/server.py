import os
import signal
import socket
import sys
import requests
import server_config
import threading
from http_helpers import HttpParser


# --------------------------------------------------------------------------------------------
def handle_response(connection, url: bytes):
    url = url.decode('utf-8')
    if not url.startswith('http://') or not url.startswith('https://'):
        url = f'https://{url}'
    req = requests.get(url)
    obj = HttpParser(req)
    res = obj.top(server_config.top)
    connection.sendto(res.encode('utf-8'), server_config.client_socket_file)
    # connection.sendto(url, server_config.client_socket_file)


# --------------------------------------------------------------------------------------------
def signal_handler(signal_num, frame):
    global completed_urls, server
    print(f'Terminated {signal_num}')
    print(f'Complete urls:{len(completed_urls)}\n{completed_urls}')
    server.close()
    sys.exit(1)


# --------------------------------------------------------------------------------------------
class Serv_threads:

    # ----------------------------------------------------------------------------------------
    def __init__(self, max_number):
        self.max_number = max_number
        self.th_lst = []

    # ----------------------------------------------------------------------------------------
    def threads(self,conn, lst):
        global data
        while len(data) > 0:
            flag = True
            url = data.pop(0)
            while flag:
                # print(self.th_lst)
                if len(self.th_lst) < self.max_number:
                    self.create_thread(conn, url, lst)
                    flag = False
                else:
                    for i in self.th_lst:
                        if not i.is_alive():
                            self.th_lst.remove(i)

    # --------------------------------------------------------------------------------------------
    def create_thread(self, conn, url: bytes, lst):
        th = threading.Thread(target=handle_response, args=(conn, url, ))
        self.th_lst.append(th)
        th.start()
        lst.append((url.decode('utf-8'), th.getName()))


# --------------------------------------------------------------------------------------------
if __name__ == '__main__':
    completed_urls = []
    server_threads = Serv_threads(server_config.server_workers)
    with open('server_info','w') as f:
        f.write(f"PID {os.getpid()} Workers {server_config.server_workers}")
    signal.signal(signal.SIGUSR1, signal_handler)

    server = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_DGRAM)
    os.unlink(server_config.server_socket_file)
    server.bind(server_config.server_socket_file)
    data = []
    while True:
        new_data, address = server.recvfrom(2048)
        data.append(new_data)
        server_threads.threads(server, completed_urls)
