#!/usr/bin/env python3

try:
	from .packet import packet
	from .utility import send_tcp, recv_tcp, _create_n_update_packet
	from . import seqnum as sq
except:
	from packet import packet
	from utility import send_tcp, recv_tcp, _create_n_update_packet
	import seqnum as sq
from typing import NoReturn, Union, Optional, Tuple, Coroutine
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
connect_to_server(namepair: Tuple[str, str]):				call to connect to server
register(namepair: Tuple[str,] or Tuple[str, str]):			register this user into server
pick_a_friend(friendname: str):					pick a friend in friend list that is about to call on
'''

class Client(Thread):
	def __init__(self, name='admin', password='admin'):
		Thread.__init__(self)
		# create the first socket that communicate with main server
		Host = socket.gethostname()		# not known yet
		Port = 9999				# server port
		mainAddr = ( Host, Port )
		self.main = socket.create_connection( mainAddr, 5, ( 'localhost', 0 ) )
		self.usrname = name
		self.usrkeyword = password
		self.window = {}
		self.seqnum = sq.seqnum()
		self.addr = None
		self.runningloop = Event()
		self.running = True

	def run(self):
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop( self.loop )
		self.runningloop.set()
		try:
			self.loop.run_forever()
		except:
			raise
		finally:
			self.loop.run_until_complete(self.loop.shutdown_asyncgens())
			self.loop.close()

	def _run_coroutine_threadsafe(self, f: Coroutine):
		try:
			fut = asyncio.run_coroutine_threadsafe(f, self.loop)
			fut.result()
		except:
			raise

	# login purpose
	def connect_to_server(self, namepair: Tuple[str, str]) -> NoReturn:
		f = self._connect_to_server(namepair)
		self._run_coroutine_threadsafe(f)

	# register client itself to server
	def register(self, namepair: Union[Tuple[str, str],Tuple[str]]) -> NoReturn:
		f = self._register(namepair)
		self._run_coroutine_threadsafe(f)

	# pick a friend to initilize tunnel
	def pick_a_friend(self, name: str) -> NoReturn:
		f = self._pick_a_friend(name)
		self._run_coroutine_threadsafe(f)

	def pause(self) -> NoReturn:
		self.loop.call_soon_threadsafe(self.loop.stop)

	def stop(self) -> NoReturn:
		self.running = False
		self.loop.call_soon_threadsafe(self.loop.stop)

	async def _connect_to_server(self, namepair: Tuple[str, str]) -> NoReturn:
		# server addr is empty
		(self.usrname, self.usrkeyword) = namepair
		# get ?
		(p, sqnum) = await _create_n_update_packet( self.window, self.seqnum, packet.CONN, str(namepair) )

		# assume that sendall always succeed
		# and it is basically the send_tcp implemented
		while True:
			try:
				self.main.sendall( p.getdata() )

				retp = recv_tcp( self.main )
				
				if retp.type == packet.ACK:
					self.window[sqnum] = None
					break
			except:
				# regardless of all errors happened in this stage
				continue

	async def _register( self, data: Union[Tuple[str, str],Tuple[str]] ) -> NoReturn:
		main = self.main

		(p, _) = await _create_n_update_packet(self.window, self.seqnum, packet.REGISTER, str(data))

		main.sendall( p.getdata() )

		retp = recv_tcp( main )
		rettype = retp.type
		if rettype == packet.EOT:
			raise registrationError(retp.data)
		elif rettype == packet.ACK:
			print( "ANYTHING!!!" )
		else:
			raise NotImplementedError

	async def _pick_a_friend(self, name: str) -> NoReturn:
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
			except Exception:
				#re-try
				continue