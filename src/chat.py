#!/usr/bin/env python3
try:
	from .packet import packet
	from .utility import send_tcp, recv_tcp, _create_n_update_packet
except:
	from packet import packet
	from utility import send_tcp, recv_tcp, _create_n_update_packet
from threading import Thread
from typing import NoReturn, Union, Optional, Tuple, Coroutine
from collections import deque
import seqnum as sq
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
		self.task_window = {}
		self.talk_channel_open = False
		self.msg = deque()
		self.recv_msg = deque()
		self.base = deque([set()]*32, maxlen=32)				# not received packet list
		self.notifing_packet = deque()
		self.msg_signal = asyncio.Condition()
		self.recv_signal = asyncio.Condition()

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
	def import_msg(self, msg: str) -> NoReturn:
		self.loop.call_soon_threadsafe(self._import_msg, msg)

	def connect2friend(self, sock:socket.socket, recvbox: deque) -> NoReturn:
		f = self._enter_talk_channel( sock, recvbox )
		self._run_coroutine_threadsafe( f )

	def stop(self) -> NoReturn:
		self.loop.call_soon_threadsafe(self.loop.stop)

	async def _import_msg(self, msg: str) -> NoReturn:
		self.msg.append(msg)
		async with self.msg_signal as ms:
			ns.notify()

	# implement selective repeat first
	async def _send_packet(self, window: dict, sock: socket.socket, seq: sq.seqnum) -> NoReturn:
		while self.talk_channel_open:
			async with self.msg_signal as ms:
				await ms.wait()

			msg = self.msg.popleft()

			(p, sqnum) = await _create_n_update_packet( window, seq, packet.PACK, msg )
			send_tcp( sock, p.getdata() )

			task = asyncio.create_task(self._time_out(window, sock, sqnum))

			if self.task_window[sqnum]:
				self.task_window[sqnum].cancel()
			self.task_window[sqnum] = task

	async def _time_out(self, window: dict, sock: socket.socket, seqnum: int) -> NoReturn:
		p = window[seqnum]
		try:
			for _ in range(2):
				await asyncio.sleep( 60 )
				# ignore that packet might send due to race condition
				# race condition will not happen since new packet at same seqnum
				# will wait until old packet is sent
				if p is None:
					break
				send_tcp( sock, p.getdata() )
		except asyncio.CancelledError:
			print('Wasted {}', seqnum)
			pass
		finally:
			if p is not None:
				raise timeoutError

	async def _get_msg(self, recv_box: deque) -> NoReturn:
		while self.talk_channel_open:
			async with self.recv_signal as rs:
				await rs.wait()
				(ver, seq, data) = self.recv_msg.popleft()
				self.base[seq].remove(ver)
			# deque is thread-safe so we could just append data in this thread
			recv_box.append(data)

	async def _send_ack(self, sock: socket.socket, seq: sq.seqnum) -> NoReturn:
		while self.talk_channel_open:
			# ack packets are not counting and storing in window
			async with self.recv_signal as rs:
				await noti.wait()
				
			seq = self.notifing_packet.popleft()

			p = packet.createACK( seq )

			sock.sendall( p.getdata() )

	async def _recv(self, window: dict, sock:socket.socket) -> NoReturn:
		while self.talk_channel_open:
			ret = recv_tcp(sock)
			rettype = ret.type

			if rettype == packet.ACK:
				window[ret.seqnum] = None
			elif rettype == packet.PACK:
				# 
				with ret.seqnum as seq:
					self.notifing_packet.append( seq )
					
					async with self.recv_signal as rs:
						if len(base[seq]) == 0:
							base[seq] = ret.version
						elif ret.version not in base[seq]:
							base[seq].add(ret.version)
						else:
							# packet aleardy stored
							continue
						rs.notify_all()

					self.recv_msg.append( (ret.version, seq, ret.data) )

			elif rettype == packet.EOT:
				self.talk_channel_open = False
			else:
				raise NotImplementedError

	# for now, only one socket is used for discussion
	# don't know it will or not lead to race condition on send or recv
	# wait until it is testified 
	# to decide how many sockets the channel needs
	async def _enter_talk_channel(self, sock: socket.socket, recv_box: deque) -> NoReturn:
		self.talk_channel_open = True
		window = {}
		seq = sq.seqnum()
		try:
			tasks = [
				self._send_packet( window, sock, seq ),
				self._recv( window, sock ),
				self._send_ack( sock ),
				self._get_msg( recv_box )
			]

			sock.gather( *tasks )
		except RuntimeError:
			raise
			
		# end of discussion
		sock.close()

