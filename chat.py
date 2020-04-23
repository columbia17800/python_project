#!/usr/bin/env python3
import socket

class Chatter():
	#""A simple TCP/UDP chat""
	
	#initial for server side
	def __init__(self, sock=None, side: bool):
		# server side is true and client side is false
		self.selfHost = socket.gethostname()
		self.selfPort = 80
		self.blockTime = 1
		try:
			if sock is None and side:
				# server need binding
				if socket.has_dualstack_ipv6():
					self.sock = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True  )
				else:
					self.sock = socket.create_server(addr)
			else if sock is None and !side:
				# client does not need it
				if socket.has_dualstack_ipv6():
					self.sock = socket.socket(addr, family=socket.AF_INET6  )
				else:
					self.sock = socket.socket(addr)
				self.serverHost = ''			# to be written
				self.serverPost = 80			# try 80 first
			else if socket is not None:
				# binding is not handled in this section
				self.sock = sock
			else:
				pass
		except ValueError as e:
			raise e
		else:
			print( 'What happened??? Another Error?!' )
		self.addr = self.sock.getsockname()[0]

	def __del__(self):
		closeSocket()

	def initialTunnel(self):
		# local reference
		# following only accept IPv4
		s = self.sock

		s.bind( ( self.selfIP, self.selfPort ) )
		s.listen( self.blockTime )
		# accept calling
		conn, addr = s.accept()

		dataList = []
		while True:
			data = conn.rev(1024)
			if not data: break
			dataList.append[data]
		
		# channel ends
		conn.close()
		# might return dataList


	def callServer(self):
		s = self.sock 					# simplify the variable name
		s.connect( ( self.targetIP, self.targetPort ) )
		
		while True:						# break if 
			s.send( self.data )
			recv = s.recv(1024)			# receive stored at local
			if str(recv) == "¿" : break
			print( repr(recv) )
		
		closeSocket(self)						# close socket


	def closeSocket(self):
		s.close()