#!/usr/bin/env python3
import socket
from typing import NoReturn, Union,Optional

class Chatter():
	#""A simple TCP/UDP chat""
	
	def __init__(self):
		# create the first socket that communicate with main server
		Host = ''				# not known yet
		Port = 80				# through http port
		self.mainAddr = ( Host, Port )

	# parameter takes addr which consists of host and port used for udp socket
	def initP2P( target:Tuple[str, int] ) -> Optional[socket.socket]:
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
			# currently, no usage of below variables
			(host, port) = sock.getsockname()
			raise NotImplemented

			askforauthority = socket.socket( socket.AF_INET, socket_DGRAM )

			# following data need to reconstruct
			askforauthority.sendto(
				b'Do you want to inital the P2P communication', target )

			# try to set some options to make to multicast-friendly
			askforauthority.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			try:
				askforauthority.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			except AttributeError:
				pass

			# listen to incoming msg
			askforauthority.bind( (selfHost, selfPort) )
			(data, addr) = askforauthority.recvfrom(1024)
			if data == b'0':
				sock.close()
				return None
			else:
				sock.listen(1)
				return sock
			
		except ValueError as e:
			raise e
		else:
			print( 'What happened??? Another Error?!' )

	def __del__(self):
		self.mainSock.close()

	def connectToServer(self) -> NoReturn:
		mainSock = socket.create_connection( self.mainAddr, 5, ( '', 0 ) )

		# say hello to server and login
		if mainSock.sendall( data ) is not None:
			mainSock.send( data )
			# assume send does send all bytes successfully for now

		data = mainSock.recv(1024)
		#assume 1024 bytes are enough

		self.main = mainSock

	def pickAfriend(self, name: str) -> NoReturn:
		main = self.main

		main.sendall(bytes(name))

		# it need parse which is not completed yet
		raise NotImplemented
		addr = main.recv(1024)

		try:
			connect2friend( self, addr )
		except ValueError as e:
			raise e

	def connect2friend(self, recvAddr: Tuple[str, int]) -> NoReturn:
		retsock = initP2P( recvAddr )
		# might use try block later on
		if retsock is None:
			# wait for the function in ui to complete the yes/no part
			# for now, it always restart the routine
			raise NotImplemented
			print('remote end refused, wanna try again?')
			# user want to connect again
			raise ValueError
		
		# establish tcp socket
		(remote, addr) = retsock.accpet()
		# since for now only a conversation is allowed
		# , we don not need to dispatch threads to handle socket
		# need threads to handle send and receive message
		raise NotImplemented

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