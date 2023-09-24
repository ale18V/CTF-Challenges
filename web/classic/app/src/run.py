import socket
import sys

HOST = sys.argv[1]
PORT = sys.argv[2]
MESSAGE = sys.argv[3]

with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
    sock.connect( (HOST,PORT) )
    sock.sendall(MESSAGE.encode())
