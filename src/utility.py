#!usr/bin/env python3
try:
	from .packet import packet
except:
	from packet import packet

from typing import NoReturn, Tuple
from asyncio import sleep
import socket

# send the data with socket provided
def send_tcp(sock: socket.socket, data: str) -> NoReturn:
	length = len(data)
	totalsent = 0
	while totalsent < length:
		sent = sock.send( data[totalsent:] )
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent += sent

async def asy_send_tcp(loop, sock: socket.socket, data: str) -> NoReturn:
	length = len(data)
	totalsent = 0
	while totalsent < length:
		sent = await loop.sock_send( sock, data[totalsent:] )
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent += sent

# receive data from the tcp socket provided
# and return the parsed packet object
def recv_tcp(sock: socket.socket) -> packet:
	length = -1
	totalrecd = 0
	retp = None
	while True:
		if totalrecd == length:
			break
		ret = sock.recv(2048)
		if ret == b'':
			# ignore empty block sent from sendall
			continue
		# when running in first time
		if length == -1:
			retp = packet.parsedata(ret)
			length = retp.length
			if retp.data is None:
				break
			recdlen = len(retp.data)
			if length == recdlen:
				break
			totalrecd += recdlen
			continue
		# else
		ret = ret.decode('UTF-8')
		totalrecd += len(ret)
		retp.data += ret

	return retp

# receive data from the tcp socket provided
# and return the parsed packet object
async def asy_recv_tcp(loop, sock: socket.socket) -> packet:
	length = -1
	totalrecd = 0
	retp = None
	while True:
		if totalrecd == length:
			break
		ret = await loop.sock_recv(sock, 2048)
		if ret == b'':
			# ignore empty block sent from sendall
			continue
		# when running in first time
		if length == -1:
			retp = packet.parsedata(ret)
			length = retp.length
			if retp.data is None:
				break
			recdlen = len(retp.data)
			if length == recdlen:
				break
			totalrecd += recdlen
			continue
		# else
		ret = ret.decode('UTF-8')
		totalrecd += len(ret)
		retp.data += ret

	return retp
