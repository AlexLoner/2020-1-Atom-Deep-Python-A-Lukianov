import requests
from struct import pack, unpack
from http_helpers import HttpParser
from server_config import recv_size


# --------------------------------------------------------------------------------------------
# def send_data(connection, data, addr):
#     ''' Extect UDP protocol'''
#     data = data.encode('utf-8')
#     size = len(data)
#     length = pack('>Q', size)
#     connection.sendto(length, addr)
#     for l, r in zip(range(0, size, recv_size), range(recv_size, size + recv_size, recv_size)):
#         connection.sendto(data[l:r], addr)

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
        to_read = response_size - len(data)
        data += connection.recv(recv_size if to_read > recv_size else to_read)
        # print(len(data), response_size)
    return data


# --------------------------------------------------------------------------------------------
def handle_response(connection, url):
    req = requests.get(url=url)
    obj = HttpParser(reqst=req)
    js_obj = obj.top10()

    return js_obj
    # send_data(connection, js_obj)
