import socket
import time

sites = ['google.com', 'python.org', 'mail.ru']
for site in sites:
    client = socket.socket()
    client.connect(('localhost', 40404))
    client.send(site.encode())
    data = client.recv(2048)
    client.close()
    print(data.decode())
