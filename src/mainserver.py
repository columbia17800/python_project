#!/usr/bin/env python3
try:
	from .utility import send_tcp, recv_tcp
	from .packet import packet, eprint
except:
	from utility import send_tcp, recv_tcp
	from packet import packet, eprint
from collections import deque
from ast import literal_eval
import socket
import socketserver
import threading

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	# assume that sending packets from server side always arrive
	def setup(self):
		self.msg = deque()
		self.running = True
		self.name = None

	def finish(self):
		pass

	def ack(self):
		raise NotImplementedError
		name = self.retp.data

		if name != "":
			(request, _) = self.server.get_client(name, (None, None))
			if request is not None:
				p = packet.createACK( self.retp.seqnum )
				request.sendall(p.getdata())
			else:
				pass
		else:
			pass

	def eot(self):
		name = self.retp.data
		if name is None:
			self.running = False
			p = packet.createEOT( self.retp.seqnum )
			self.request.sendall( p.getdata() )
			self.server.close_request( self.request )
			if self.name:
				self.server.remove_client( self.name )
		else:
			(request, _) = self.server.get_client( name )
			p = packet.createEOT( self.retp.seqnum )
			request.sendall(p.getdata())

	def pack(self):
		self.msg.append( self.retp.data )

		p = packet.createACK( self.retp.seqnum )

		self.request.sendall( p.getdata() )

	# login
	def connrequest(self):
		(name, keyword) = literal_eval(self.retp.data)
		password = self.server.get_password(name)
		p = None
		if password is None or password != keyword:
			p = packet.createEOT( self.retp.seqnum )
		else:
			p = packet.createACK( self.retp.seqnum )
			self.name = name
			self.server.set_client(name, (self.request, self.client_address))
		self.request.sendall( p.getdata() )

	def get(self):
		name = self.retp.data

		(_, addr) = self.server.get_client(name)

		if addr is None:
			p = packet.createEOT( self.retp.seqnum )
		else:
			p = packet.createACK( self.retp.seqnum, str(addr) )
		self.request.sendall( p.getdata() )

	def register(self):
		data = literal_eval(self.retp.data)
		name = data[0]
		password = self.server.get_password(name)
		p = None
		if password is not None:
			p = packet.createEOT( self.retp.seqnum, "selected name is registered" )
		elif len(data) > 1:
			self.server.set_password(name, data[1])
			p = packet.createACK( self.retp.seqnum )
		else:
			p = packet.createEOT( self.retp.seqnum, "write your password in the field" )
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
		while self.running:
			try:
				self.retp = recv_tcp( self.request )
				switcher[self.retp.type]()
			except:
				raise

class MainServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

	def __init__(self):
		# selfHost = socket.gethostbyname(socket.gethostname())
		self.__class__.allow_reuse_address = True
		super().__init__(("localhost", 9999), ThreadedTCPRequestHandler)
		self.clients_available = {}
		self.name_list = {}
		self.clients_lock = threading.Lock()
		self.password_lock = threading.Lock()

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
