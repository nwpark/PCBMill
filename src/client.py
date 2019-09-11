import socket

PI = '192.168.1.89'
LOCALHOST = '127.0.0.1'
PORT = 65432


def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder='big')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((PI, PORT))
    # s.sendall(b'Hello, world')
    s.sendall(bytes([0]))
    data = bytes_to_int(s.recv(1024))

print('Received', repr(data))