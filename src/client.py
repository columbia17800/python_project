#!/usr/bin/env python3

try:
	from packet import packet
	from typing import NoReturn, Union, Optional, Tuple
	from utility import send_tcp, recv_tcp, _create_n_update_packet
	import seqnum as sq
except:
	from .uisetting import UISetting
	from .typing import NoReturn, Union, Optional, Tuple
	from .chat import Chatter
	from . import seqnum as sq
from collections import deque
from threading import Thread, Event
from ast import literal_eval
import asyncio
import socket

class registrationError(Exception):
	def __init__(self, reason):
		super().__init__(self)
		self.reason = reason
	pass

'''
connect_to_server:				call to connect to server
register:						register this user into server
pick_a_friend:					pick a friend in friend list that is about to call on

'''

class Client(Thread):
	def __init__(self):
		Thread.__init__(self)
		# create the first socket that communicate with main server
		Host = 'localhost'		# not known yet
		Port = 9999				# through http port
		self.mainAddr = ( Host, Port )
		self.name = ""
		self.keyword = ""
		self.window = {}
		self.seqnum = sq.seqnum()
		self.addr = None
		self.runningloop = Event()

	def run(self):
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop( self.loop() )
		runningloop.set()
		try:
			self.loop.run_forever()
		finally:
			self.loop.run_until_complete(loop.shutdown_asyncgens())
			self.loop.close()

	def connect_to_server(self) -> NoReturn:
		self.loop.call_soon_threadsafe(self._connect_to_server)

	def register(self, namepair: Union[Tuple[str, str],Tuple[str]]) -> NoReturn:
		self.loop.call_soon_threadsafe(self._register, namepair)

	def pick_a_friend(self, name: str, event: Event) -> NoReturn:
		self.loop.call_soon_threadsafe(self._pick_a_friend, name, event)

	def stop(self) -> NoReturn:
		self.loop.call_soon_threadsafe(self.loop.stop)

	async def _connect_to_server(self) -> NoReturn:
		# server addr is empty
		mainSock = socket.create_connection( self.mainAddr, 5, ( '', 0 ) )
		raise NotImplementedError
		
		login = (self.name, self.keyword)
		# get ?
		(p, sqnum) = await _create_n_update_packet( self.window, self.seqnum, packet.CONN, str(login) )

		# assume that sendall always succeed
		# and it is basically the send_tcp implemented
		while True:
			try:
				mainSock.sendall( p.getdata() )

				retp = recv_tcp( mainSock )
				
				if retp.type == packet.ACK:
					self.window[sqnum] = None
					break
			except:
				# regardless of all errors happened in this stage
				continue

		self.main = mainSock

	async def _register( self, data: Union[Tuple[str, str],Tuple[str]] ) -> NoReturn:
		main = self.main

		p = _create_n_update_packet(self.window, self.seqnum, packet.REGISTER, str(data))

		main.sendall( p.getdata() )

		retp = recv_tcp( main )
		rettype = retp.type
		if retp == packet.EOT:
			raise registrationError(retp.data)
		elif retp == packet.ACK:
			print( "ANYTHING!!!" )
		else:
			raise NotImplementedError

	async def _pick_a_friend(self, name: str, event: Event) -> NoReturn:
		main = self.main

		(p, sqnum) = await _create_n_update_packet( self.window, self.seqnum, packet.GET, name )
		
		while True:
			try:
				# send packet
				send_tcp( main, p.getdata() )

				# receive packet
				retp = recv_tcp( main )
				rettype = retp.type

				if rettype == packet.EOT:
					self.window[sqnum] = None
					print("your friend is offline, \
						pick another available friend")
					raise NotImplementedError
					# require operations from UI
				elif rettype == packet.ACK:
					self.window[sqnum] = None
					self.addr = literal_eval(retp.data)
				else:
					# I did not even think of this event
					raise NotImplementedError
				event.set()
			except Exception:
				#re-try
				continue