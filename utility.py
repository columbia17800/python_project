#!usr/bin/env python3
from typing import NoReturn
import socket
import packet

# send the data with socket provided
def send_tcp(sock: socket.socket, data: str) -> NoReturn:
	length = len(data)
	totalsent = 0
	while totalsent < length:
		sent = sock.send( data[totalsent:] )
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent += sent

# receive data from the tcp socket provided
# and return the parsed packet object
def recv_tcp(sock: socket.socket) -> packet:
	length = 0
	totalrecd = 0
	retp = None
	while True:
		if totalrecd == length:
			break
		ret = sock.recv(2048)
		if ret == b'':
			raise RuntimeError("socket connection broken")
		# when running in first time
		if length == 0:
			retp = packet.parsedata(ret)
			length = retp.length
			recdlen = len(retp.data)
			if length == recdlen:
				return retp
			totalrecd += recdlen
			continue
		# else
		ret = ret.decode('UTF-8')
		totalrecd += len(ret)
		retp.data += ret

	return retp