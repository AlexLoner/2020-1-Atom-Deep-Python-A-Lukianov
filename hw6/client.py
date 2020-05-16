import os
import socket
from help_func import get_data, send_data

sites = ['google.com', 'python.org', 'mail.ru']
for site in sites:

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5013))

    send_data(client, site)
    data = get_data(client).decode()

    client.close()
    folder = 'json_folder'
    if folder not in os.listdir():
        os.mkdir(folder)
    with open(f"{folder}/{site.split('.')[0]}.json", "w") as f:
        f.write(data)

