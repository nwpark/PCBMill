import socket

PI = '192.168.1.89'
LOCALHOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((PI, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))