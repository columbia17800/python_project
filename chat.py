#!/usr/bin/env python3
import socket
from packet import packet
from typing import NoReturn, Union,Optional
import seqnum as sq


class Chatter():
	#""A simple TCP/UDP chat""
	
	def __init__(self):
		# create the first socket that communicate with main server
		Host = ''				# not known yet
		Port = 80				# through http port
		self.mainAddr = ( Host, Port )
		self.window = {}				# window used for storing packets
		self.seqnum = sq.seqnum()

	def _send_n_recv_udp(self, sock: socket.socket, target: Tuple[str, int], data: str) -> Optional[packet]:
		while True:
			try:
				# following data need to reconstruct
				sock.sendto(
					data, target )

				(ret, _) = sock.recvfrom(1024)

				retp = packet.parsedata(ret)

				# close the udp socket since it should not be used for now on
				sock.close()

			except socket.timeout:
				continue
			else:
				print("NOOOOOOOOOOOOO WAAAAAAAAAAAAAAY")
				return None
			return retp

	# send the data with socket provided
	def _send_tcp(sock: socket.socket, data: str) -> NoReturn:
		length = len(data)
		totalsent = 0
		while totalsent < length:
			sent = sock.send( data[totalsent:] )
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent += sent

	# receive data from the tcp socket provided
	# and return the parsed packet object
	def _recv_tcp(sock: socket.socket) -> packet:
		length = 0
		totalrecd = 0
		retp = None
		while True:
			if totalrecd == length:
				break
			ret = sock.recv(2048):
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


	# parameter takes addr which consists of host and port used for udp socket
	def initP2P( self, target:Tuple[str, int] ) -> Optional[socket.socket]:
		# server side is true and client side is false
		selfHost = socket.gethostbyname(gethostname())
		selfPort = 0
		##
		addr = ( selfHost, selfPort )
		try:
			# server need binding explicitly
			if socket.has_dualstack_ipv6():
				sock = socket.create_server(
					addr, family=socket.AF_INET6, dualstack_ipv6=True )
			else:
				sock = socket.create_server(addr)

			addr = sock.getsockname()
			seqnum = self.seqnum.getNum()
			p = packet.createConnRequest(seqnum, str(addr))
			if self.window.get(seqnum) is not None:
				raise AttributeError
			self.window[seqnum] = p
			self.seqnum.goNext()
			# pack the host and port and send to friend that u  wanna connect with
			
			askforauthority = socket.socket( socket.AF_INET, socket_DGRAM )
			askforauthority.settimeout(42.0)

			# try to set some options to make to multicast-friendly
			askforauthority.setsockopt(
				socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			try:
				askforauthority.setsockopt(
					socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			except AttributeError:
				pass

			# listen to incoming msg
			askforauthority.bind( (selfHost, selfPort) )
			
			# send packet to target and get returned packet
			retp = _send_n_recv_udp( self, askforauthority, target, p.getdata() )
			if retp is None:
				# did not come up a good way to handle this
				# leave like this right now
				raise ValueError
			rettype = retp.type

			if rettype == packet.EOT:
				sock.close()
				p.recved()
				return None
			else if rettype == packet.ACK:
				p.recved()
				sock.listen(1)
				return sock
			else:
				# I did not even think of this event
				raise NotImplementedError
				
		except ValueError as e:
			raise e
		else:
			print( 'What happened??? Another Error At initP2P?!' )

	def __del__(self):
		self.mainSock.close()

	def connectToServer(self) -> NoReturn:
		mainSock = socket.create_connection( self.mainAddr, 5, ( '', 0 ) )

		# say hello to server and login
		if mainSock.sendall( data ) is not None:
			mainSock.send( data )
			# assume send does send all bytes successfully for now
		raise NotImplementedError
		data = mainSock.recv(1024)
		#assume 1024 bytes are enough

		self.main = mainSock

	def pickAfriend(self, name: str) -> NoReturn:
		main = self.main

		seqnum = self.seqnum.getNum()
		p = packet.createGet(seqnum, name)
		# not gonna handle it because this shold not happen
		# hence let it crash
		if window.get(seqnum) is not None:
			raise AttributeError
		window[seqnum] = p
		self.seqnum.goNext()
		while True:
			try:
				# send packet
				_send_tcp( main, p.getdata() )

				# parse the return packet
				retp = _recv_tcp( main )
				rettype = retp.type

				if rettype == packet.EOT:
					p.recved()
					print("your friend is offline, \
						pick another available friend")
					raise NotImplementedError
					# require operations from UI
					break
				else if rettype == packet.ACK:
					p.recved()
					addr = literal_eval(retp.data)
					break
				else:
					# I did not even think of this event
					raise NotImplementedError

			except Exception:
				#re-try
				continue

		connect2friend( self, addr )

	def connect2friend(self, recvAddr: Tuple[str, int]) -> NoReturn:
		retsock = self.initP2P( recvAddr )
		# might use try block later on
		if retsock is None:
			# wait for the function in ui to complete the yes/no part
			# for now, it always restart the routine
			raise NotImplementedError
			print('remote end refused, wanna try again?')
			# user want to connect again
			raise ValueError
		
		# establish tcp socket
		(remote, addr) = retsock.accpet()
		# since for now only a conversation is allowed
		# , we don not need to dispatch threads to handle socket
		# need threads to handle send and receive message
		raise NotImplementedError

	def waiter(self) -> NoReturn:
		# local reference
		# following only accept IPv4 right now
		s = self.sock

		s.listen( self.blockTime )
		# accept calling
		clientsock, addr = s.accept()

		dataList = []
		while True:
			data = clientsock.rev(1024)
			if not data: break
			dataList.append[data]


		
		# channel ends
		clientsock.close()
		# might return dataList


	def callServer(self):
		s = self.sock 					# simplify the variable name
		s.connect( ( self.targetIP, self.targetPort ) )
		
		while True:						# break if 
			s.send( self.data )
			recv = s.recv(1024)			# receive stored at local
			if str(recv) == "¿" : break
			print( repr(recv) )
		
		# close socket

	def notify(which: int)：
		# functions for notify timeout for packets
		window[which].check()