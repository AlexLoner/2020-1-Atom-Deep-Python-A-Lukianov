import socket

from help_func import get_data, send_data

sites = ['google.com', 'python.org']#, 'mail.ru']
for site in sites:

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5013))

    send_data(client, site)
    data = get_data(client).decode()

    client.close()
    print(data)

    with open(f"{site.split()[0]}.json", "w") as f:
        f.write(data)

