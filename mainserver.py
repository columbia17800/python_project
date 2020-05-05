#!/usr/bin/env python3
from utility import send_tcp, recv_tcp
from collections import deque
import socket
import socketserver
import packet

class MainServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
		# assume that sending packets from server side always arrive
		def setup(self):
			self.msg = deque()

		def finish(self):
			pass

		def ack(self):
			raise NotImplementedError

		def eot(self):
			self.request.close()
			self.server.clients_available.remove(name)

		def pack(self):
			self.msg.append( self.retp.data )

			p = createACK( self.retp.seqnum )

			self.request.sendall( p.getdata() )

		def connrequest(self):
			(name, keyword) = self.retp.data.literal_eval()
			password = self.server.name_list.get(name, None)
			p = None
			if password is None or password != keyword:
				p = createEOT( self.retp.seqnum )
			else:
				p = createACK( self.retp.seqnum )
				self.name = name
				self.server.clients_available[name] = self.client_addr
			self.request.sendall( p.getdata() )

		def get(self):
			name = self.retp.data

			addr = self.server.clients_available.get(name, None)

			if addr is None:
				p = createEOT( self.retp.seqnum )
			else:
				p = createACK( self.retp.seqnum, str(addr) )
			self.request.sendall( p.getdata() )

		def register(self):
			data = self.retp.data.literal_eval()
			name = data[0]
			password = self.server.name_list.get(name, None)
			p = None
			if password is not None:
				p = createEOT( self.retp.seqnum, "selected name is registered" )
			elif len(data) > 1:
				self.server.name_list[name] = data[1]
				p = createACK( self.retp.seqnum )
			else:
				p = createEOT( self.retp.seqnum, "write your password in the field" )
			self.request.sendall( p.getdata() )


		def handle(self):
			switcher = {
				0 : self.ack,
				1 : self.pack,
				2 : self.eot,
				3 : self.connrequest,
				4 : self.get,
				5 : self.register,
			}
			self.retp = recv_tcp( self.request )

			switcher[retp.type]()

	def __init__(self):
		selfHost = socket.gethostbyname(socket.gethostname())
		selfPort = 80
		addr = ( self.selfHost, self.selfPort )
		super().__init__(self, addr, ThreadedTCPRequestHandler)
		self.clients_available = {}
		self.name_list = {}

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
'''
	def endServer(self):
		self.sock.close()
'''