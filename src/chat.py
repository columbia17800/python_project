#!/usr/bin/env python3
try:
	from .packet import packet
	from .utility import asy_send_tcp, asy_recv_tcp
except:
	from packet import packet
	from utility import asy_send_tcp, asy_recv_tcp
from threading import Thread
from typing import NoReturn, Union, Optional, Tuple, Coroutine
from collections import deque
import asyncio
import socket

class timeoutError(Exception):
	pass

'''
init_P2P:						inital peer-to-peer channel				
'''
class Chatter(Thread):
	#""A simple TCP/UDP P2P chat""

	def __init__(self):
		Thread.__init__(self)
		self.talk_channel_open = False
		self.poolsize = asyncio.Semaphore(5)
		self.pool = {}
		self.msg = {}
		self.recv_msg = {}
		self.poolLock = asyncio.Lock()
		self.msg_signal = asyncio.Condition()

	def __del__(self):
		raise NotImplementedError

	def _run_coroutine_threadsafe(self, f: Coroutine):
		try:
			fut = asyncio.run_coroutine_threadsafe(f, self.loop)
			fut.result()
		except:
			raise

	def run(self):
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop( self.loop() )
		try:
			self.loop.run_forever()
		finally:
			self.loop.run_until_complete(loop.shutdown_asyncgens())
			self.loop.close()

	# methods for UI in another thread to call inner methods safely
	def import_msg(self, msg: str, name: str) -> NoReturn:
		self.loop.call_soon_threadsafe(self._import_msg, msg, name)

	def connect2friend(self, sock:socket.socket, name: str) -> NoReturn:
		f = self._enter_talk_channel( sock, name )
		self._run_coroutine_threadsafe( f )

	def stop(self) -> NoReturn:
		self.loop.call_soon_threadsafe(self.loop.stop)

	async def _import_msg(self, msg: str, name: str) -> NoReturn:
		self.msg[name].append(msg)
		async with self.msg_signal as ms:
			ns.notify_all()

	# implement selective repeat first
	async def _send_packet(self, sock: socket.socket, name: str):
		while True:
			# busy waiting until get msgs
			while len(self.msg[name]) == 0:
				async with self.msg_signal as ms:
					await ms.wait()

			msg = self.msg[name].popleft()

			p = packet.createPacket( msg )
			asyncio.create_task( asy_send_tcp( self.loop, sock, p.getdata() ) )

	async def _recv(self, sock:socket.socket, name: str):
		while True:
			rettask = asyncio.create_task( asy_recv_tcp( self.loop, sock) )
			await rettask
			
			try:
				ret = rettask.result()
			except asyncio.CancelledError:
				raise
			rettype = ret.type

			if rettype == packet.ACK:
				pass
			elif rettype == packet.PACK:
				self.recv_msg[name].append( ret.data )

			elif rettype == packet.EOT:
				self.talk_channel_open = False
				break
			else:
				raise NotImplementedError

	# for now, only one socket is used for discussion
	# don't know it will or not lead to race condition on send or recv
	# wait until it is testified 
	# to decide how many sockets the channel needs
	async def _enter_talk_channel(self, sock: socket.socket, name: str) -> NoReturn:
		self.talk_channel_open = True
		try:
			await sem,acquire()
			tasks = [
				asyncio.create_task(self._send_packet( sock, name )),
				asyncio.create_task(self._recv( sock, name )),
			]

			tasks = asyncio.gather( *tasks )
			async with poolLock:
				self.pool[name] = tasks
				self.msg[name] = deque()
				self.recv_msg[name] = deque()
			await tasks
		except RuntimeError:
			raise
		except asyncio.CancelledError:
			pass
		finally:
			# end of discussion
			sock.close()
			sem.release()

	async def _stop(self, name):
		channel = self.pool.get(name, None)
		if channel:
			channel.cancel()
			channel.exception()
		else:
			raise NotImplementedError
		async with poolLock:
			del self.pool[name]
			del self.msg[name]
			del self.recv_msg[name]

