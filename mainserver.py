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
			self.running = True

		def finish(self):
			pass

		def ack(self):
			raise NotImplementedError
			name = self.retp.data

			if name != "":
				(request, _) = self.server.get_client(name, (None, None))
				if request is not None:
					p = createACK( self.retp.seqnum )
					request.sendall(p.getdata())
				else:
					pass
			else:
				pass

		def eot(self):
			name = self.retp.data
			if name == "":
				self.running = False
				self.server.remove_client( self.name )
				self.server.close_request( self.request )
			else:
				(request, _) = self.server.get_client( name )
				p = createEOT( self.retp.seqnum )
				request.sendall(p.getdata())

		def pack(self):
			self.msg.append( self.retp.data )

			p = createACK( self.retp.seqnum )

			self.request.sendall( p.getdata() )

		def connrequest(self):
			(name, keyword) = self.retp.data.literal_eval()
			password = self.server.get_password(name)
			p = None
			if password is None or password != keyword:
				p = createEOT( self.retp.seqnum )
			else:
				p = createACK( self.retp.seqnum )
				self.name = name
				self.server.set_client(name, (self.request, self.client_addr))
			self.request.sendall( p.getdata() )

		def get(self):
			name = self.retp.data

			(_, addr) = self.server.get_client(name)

			if addr is None:
				p = createEOT( self.retp.seqnum )
			else:
				p = createACK( self.retp.seqnum, str(addr) )
			self.request.sendall( p.getdata() )

		def register(self):
			data = self.retp.data.literal_eval()
			name = data[0]
			password = self.server.get_password(name)
			p = None
			if password is not None:
				p = createEOT( self.retp.seqnum, "selected name is registered" )
			elif len(data) > 1:
				self.server.set_password(name, data[1])
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
			while running:
				try:
					self.retp = recv_tcp( self.request )
					switcher[retp.type]()
				except:
					raise

	def __init__(self):
		selfHost = socket.gethostbyname(socket.gethostname())
		selfPort = 80
		addr = ( self.selfHost, self.selfPort )
		super().__init__(self, addr, ThreadedTCPRequestHandler)
		self.clients_available = {}
		self.name_list = {}
		self.clients_lock = threading.lock()
		self.password_lock = threading.lock()

	def get_client( self, name: str ):
		with self.clients_lock:
			return self.clients_available.get(name, (None, None))

	def set_client( self, name: str, pair ):
		with self.clients_lock:
			self.clients_available[name] = pair

	def remove_client( self, name: str ):
		with self.clients_lock:
			return self.clients_available.pop(name, (None, None))

	def set_password( self, name: str, password: str ):
		with self.password_lock:
			self.name_list[name] = password

	def get_password( self, name: str ):
		with self.password_lock:
			return self.name_list.get(name, None)