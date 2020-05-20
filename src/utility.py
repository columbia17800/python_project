#!usr/bin/env python3
try:
	from .seqnum import seqnum
	from .packet import packet
except:
	from seqnum import seqnum
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

async def _create_n_update_packet(window: dict, seq: seqnum, packet_type: int, data=None) -> Tuple[packet, int]:
	(sqn, version) = seq.getNum()
	p = packet(packet_type, sqn, data,
		0 if data is None else len(data), version)

	while window.get(sqn, None) is not None:
		await asyncio.sleep( 1 )

	window[sqn] = p
	seq.goNext()
	return (p, sqn)