#!/usr/bin/env python3
from utility import send_tcp, recv_tcp
import socket
import socketserver
import packet

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	def setup(self):
		self.switcher = {
			0 = NotImplemented,
			1 = NotImplemented,
			2 = NotImplemented,
			3 = NotImplemented,
			4 = NotImplemented,
		}
		
	def handle(self):
		retp = recv_tcp( self.request )


class ThreadedTcpServer(socketserver.ThreadingMixin, socketserver.TCPServer):
	pass

class mainServer():
	

	def __init__(self):
		self.selfHost = socket.gethostbyname(socket.gethostname())
		self.selfPort = 80
		self.allowedClients = 1								# the number of clients the listen port is allowed
		addr = ( self.selfHost, self.selfPort )
		try:
			if socket.has_dualstack_ipv6():
				self.sock = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True  )
			else:
				self.sock = socket.create_server(addr)
			self.addr = self.sock.getsockname()[0]
		except ValueError as e:
			raise e
		else:
			print( 'there should not be any other errors' )
		self.clients_available = {}

	def waiter(self):
		
		self.sock.listen( self.allowedClients )
		while True:
			# accept connections from outside
			(conn, addr) = self.sock.accept()

			raise NotImplementedError
"""
			# not done yet
			ct = manageClients(conn)
			ct.run()
"""
	def endServer(self):
		self.sock.close()