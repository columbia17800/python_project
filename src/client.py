#!/usr/bin/env python3

try:
	from .packet import packet
	from .utility import asy_recv_tcp, asy_send_tcp
	from .chat import Chatter
except:
	from packet import packet
	from utility import asy_recv_tcp, asy_send_tcp
	from chat import Chatter
from typing import NoReturn, Union, Optional, Tuple, Coroutine
from collections import deque
from threading import Thread, Event
import asyncio
import socket

class registrationError(Exception):
	def __init__(self, reason):
		super().__init__(self)
		self.reason = reason
	pass

class loginError(Exception):
	pass

class pickupError(Exception):
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
		self.addr = None
		self.runningloop = Event()
		self.running = True
		self.availchat = deque()

	def run(self):
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop( self.loop )
		self.runningloop.set()
		try:
			recyc = self.loop.create_task( self._recyclebin() )
			self.loop.run_forever()
		except:
			raise
		finally:
			recyc.cancel()
			self.loop.run_until_complete(self.loop.shutdown_asyncgens())
			self.loop.close()

	def _run_coroutine_threadsafe(self, f: Coroutine):
		try:
			fut = asyncio.run_coroutine_threadsafe(f, self.loop)
			return fut.result()
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
	def pick_a_friend(self, name: str) -> Chatter:
		f = self._pick_a_friend(name)
		return self._run_coroutine_threadsafe(f)

	def pause(self) -> NoReturn:
		self.loop.call_soon_threadsafe(self.loop.stop)

	def stop(self) -> NoReturn:
		f = self._manualstop()
		self._run_coroutine_threadsafe(f)
		self.pause()

	def recyc(self) -> NoReturn:
		f = self._manualrecyc()
		self._run_coroutine_threadsafe(f)

	async def _connect_to_server(self, namepair: Tuple[str, str]) -> NoReturn:
		# server addr is empty
		(self.usrname, self.usrkeyword) = namepair
		# get ?
		p = packet.createConnRequest( str(namepair) )

		# assume that sendall always succeed
		# and it is basically the send_tcp implemented
		await self.loop.sock_sendall( self.main, p.getdata() )

		retp = await asy_recv_tcp( self.loop, self.main )
		
		if retp.type == packet.ACK:
			print('server connected')
		elif retp.type == packet.EOT:
			raise loginError
		else:
			raise NotImplementedError

	async def _register( self, data: Union[Tuple[str, str],Tuple[str]] ) -> NoReturn:
		main = self.main

		p = packet.createRegister(str(data))

		await self.loop.sock_sendall( main, p.getdata() )

		retp = await asy_recv_tcp( self.loop, main )

		rettype = retp.type
		if rettype == packet.EOT:
			raise registrationError(retp.data)
		elif rettype == packet.ACK:
			print( "ANYTHING!!!" )
		else:
			raise NotImplementedError

	async def _pick_a_friend(self, name: str) -> NoReturn:
		main = self.main

		p2p = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		p2p.setsockopt(
			socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			p2p.setsockopt(
				socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			p2p.bind( socket.gethostname(), 0 )
			p2p.listen(1)
		except AttributeError:
			pass
		else:
			print('_pick_a_friend binding errors')
			raise

		p = packet.createGet( str( (name,) + p2p.getsockname() ) )
		
		# send packet
		await asy_send_tcp( self.loop, main, p.getdata() )

		# receive packet
		retp = await asy_recv_tcp( self.loop, main )
		rettype = retp.type

		if rettype == packet.EOT:
			print("your friend is offline, \
				pick another available friend")
			raise pickupError
			# require operations from UI
		elif rettype == packet.ACK:
			conn, _ = await self.loop.sock_accept(p2p)

			for c in self.availchat:
				if not c.poolsize.locked():
					return (c, conn)

			chat = Chatter()
			self.availchat.append(chat)
			chat.start()

			return (chat, conn)
		else:
			# I did not even think of this event
			raise NotImplementedError

	async def _recyclebin(self):
		while True:
			await asyncio.sleep(1200)
			if len(self.availchat[-1].pool) == 0:
				chat = self.availchat.pop()
				chat.stop()

	async def _manualrecyc(self):
		if len(self.availchat[-1].pool) == 0:
			chat = self.availchat.pop()
			chat.stop()

	async def _manualstop(self):
		for c in self.availchat:
			c.stop()

	async def _recv_from(self):
		raise NotImplementedError
		while True:
			retp = await asy_recv_tcp( self.loop, main )

			if rettype == packet.EOT:
				print("your friend is offline, \
					pick another available friend")
				raise pickupError
				# require operations from UI
			elif rettype == packet.ACK:
				conn, _ = await self.loop.sock_accept(p2p)

				for c in self.availchat:
					if not c.poolsize.locked():
						return (c, conn)

				chat = Chatter()
				self.availchat.append(chat)
				chat.start()

				return (chat, conn)
			else:
				# I did not even think of this event
				raise NotImplementedError