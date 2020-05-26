import os
import time
import socket
import argparse
import server_config
import multiprocessing as mp


# --------------------------------------------------------------------------------------------
def send_url(connection, data):
    connection.send(data.encode('utf-8'))
    data, addr = connection.recvfrom(2048)
    print(data.decode('utf-8'))


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--m', dest='workers', type=int)
    parser.add_argument('--file', dest='urls_file', type=str)
    args = parser.parse_args()

    client = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_DGRAM)
    client.connect(server_config.server_socket_file)

    os.unlink(server_config.client_socket_file)
    client.bind(server_config.client_socket_file)

    t1 = time.time()

    with open(args.urls_file) as file:
        tmp = [i.strip() for num, i in enumerate(file)]# if num < 20]

    procs = [mp.Process(target=send_url, args=(client, tmp[i])) for i in range(args.workers)]
    cur = args.workers
    for proc in procs:
        proc.start()
    while cur < len(tmp):
        for i in range(args.workers):
            if not procs[i].is_alive():
                procs[i] = mp.Process(target=send_url, args=(client, tmp[cur]))
                procs[i].start()
                cur += 1
    t3 = time.time() - t1
    for p in procs:
        p.join()
    print(t3)
    client.close()
