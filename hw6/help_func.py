def get_data(connection, size):
    total_data = []
    while True:
        data = connection.recv(size)
        if not data:
            break
        total_data.extend([data.decode()])
    return total_data
