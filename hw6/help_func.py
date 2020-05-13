import socket
from struct import pack, unpack


# --------------------------------------------------------------------------------------------
def send_data(connection, data):

    data = data.encode('utf-8')
    length = pack('>Q', len(data))
    connection.sendall(length)
    connection.sendall(data)


# --------------------------------------------------------------------------------------------
def get_data(connection):
    response = connection.recv(8)
    response_size = unpack('>Q', response)[0]
    data = b''
    while len(data) < response_size:
    # while True:
        to_read = response_size - len(data)
        data += connection.recv(32 if to_read > 32 else to_read)
        # try:
        #     connection.settimeout(5)
        #     data += connection.recv(32)
        # except socket.timeout:
        #     break
    return data

