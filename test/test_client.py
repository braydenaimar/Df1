#!/usr/bin/python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.1.87', 17560))
s.sendall('N7:6'.encode())
data = s.recv(1024)
s.close()
print('Received', repr(data))
