#!/usr/bin/python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))

s.listen(5)
conn, addr = s.accept()
while 1:
	print('Got connection from', addr)
	data = conn.recv(1024)
	if not data:
		break
	conn.sendall(data)

conn.close()
