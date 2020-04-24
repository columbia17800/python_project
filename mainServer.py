#!/usr/bin/env python3
import socket
import thread

class mainServer():

	class manageClients(thread.Thread):
		def __init__(self):


	def __init__(self):
		self.selfHost = socket.gethostname()
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