#!/usr/bin/env python3
import socket
from packet import packet
from typing import NoReturn, Union,Optional
from utility import send_tcp, recv_tcp
from collections import deque
import seqnum as sq
import asyncio

class timeoutError(Exception):
	pass

class Chatter():
	#""A simple TCP/UDP chat""

	def __init__(self):
		# create the first socket that communicate with main server
		Host = ''				# not known yet
		Port = 80				# through http port
		self.name = ""
		self.keyword = ""
		self.mainAddr = ( Host, Port )
		self.window = {}				# window used for storing packets
		self.task_window = {}
		self.seqnum = sq.seqnum()
		self.talk_channel_open = False
		self.msg = deque()
		self.recv_msg = deque()
		self.base = deque([set()]*32, maxlen=32)				# not received packet list
		self.notifing_packet = deque()
		self.msg_signal = async.Condition()
		self.recv_signal = async.Condition()

	def __del__(self):
		self.mainSock.close()

	async def get_msg(self) -> str:
		ret = None
		
		async with self.recv_signal as rs:
			rs.wait()
			(ver, seq, data) = self.recv_msg.popleft()
			self.base[seq].remove(ver)
			ret = data

		return ret

	async def import_msg(self, msg: str) -> NoReturn:
		async with self.msg_signal as ms:
			ns.notify()
		self.msg.append(msg)

	async def _create_n_update_packet(window: dict, seq: sq.seqnum, packet_type: int, data=None) -> Tuple[packet, int]:
		(seqnum, version) = seq.getNum()
		p = packet(packet_type, seqnum, data,
			0 if data is None else len(data), version)

		while window.get(seqnum, None) is not None:
			await asyncio.sleep( 1 )

		window[seqnum] = p
		seq.goNext()
		return (p, seqnum)

	def _send_n_recv_udp(self, sock: socket.socket, target: Tuple[str, int], data: str) -> Optional[packet]:
		while True:
			try:
				# following data need to reconstruct
				sock.sendto(
					data, target )

				(ret, _) = sock.recvfrom(1024)

				retp = packet.parsedata(ret)

				# close the udp socket since it should not be used for now on
				sock.close()

			except socket.timeout:
				continue
			else:
				print("NOOOOOOOOOOOOO WAAAAAAAAAAAAAAY")
				return None
			return retp

	# parameter takes addr which consists of host and port used for udp socket
	async def initP2P( self, target:Tuple[str, int] ) -> Optional[Tuple[socket.socket, sq.seqnum]]:
		# server side is true and client side is false
		selfHost = socket.gethostbyname(socket.gethostname())
		selfPort = 0
		##
		addr = ( selfHost, selfPort )
		try:
			# server need binding explicitly
			if socket.has_dualstack_ipv6():
				sock = socket.create_server(
					addr, family=socket.AF_INET6, dualstack_ipv6=True )
			else:
				sock = socket.create_server(addr)

			addr = sock.getsockname()
			data = str(addr)
			p = createConnRequest( 0, data )
			# pack the host and port and send to friend that u  wanna connect with
			
			askforauthority = socket.socket( socket.AF_INET, socket_DGRAM )
			askforauthority.settimeout(42.0)

			# try to set some options to make to multicast-friendly
			askforauthority.setsockopt(
				socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			try:
				askforauthority.setsockopt(
					socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
			except AttributeError:
				pass

			# listen to incoming msg
			askforauthority.bind( (selfHost, selfPort) )
			
			# send packet to target and get returned packet
			retp = self._send_n_recv_udp( askforauthority, target, p.getdata() )
			if retp is None:
				# did not come up a good way to handle this
				# leave like this right now
				raise ValueError

			rettype = retp.type

			if rettype == packet.EOT:
				sock.close()
				return None
			elif rettype == packet.ACK:
				seq = sq.seqnum()
				sock.listen(1)
				return (sock, seq)
			else:
				# I did not even think of this event
				raise NotImplementedError
				
		except ValueError as e:
			raise e
		else:
			print( 'What happened??? Another Error At initP2P?!' )

	async def connectToServer(self) -> NoReturn:
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

	async def pickAfriend(self, name: str) -> NoReturn:
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
					break
				elif rettype == packet.ACK:
					self.window[sqnum] = None
					addr = literal_eval(retp.data)
					break
				else:
					# I did not even think of this event
					raise NotImplementedError

			except Exception:
				#re-try
				continue

		await connect2friend( self, addr )

	# implement selective repeat first
	async def _send_packet(self, window: dict, sock: socket.socket, seq: sq.seqnum) -> NoReturn:
		while self.talk_channel_open:
			async with self.msg_signal as ms:
				await ms.wait():

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
'''
	async def _recv_ack(self, sock: socket.socket, seqnum: int):
		while !self.window[seqnum].ACKed:
			await asyncio.sleep(2)
			retp = recv_tcp( sock )
			if retp.type is packet.EOT:
				break
			elif retp.type is packet.ACK:
				self.window[seqnum].recved()
			else:
				raise RuntimeError(
					'this task supposed not to receive \
					packets other than ACK')
'''
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
						elif ret.version is not in base[seq]:
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
	async def _enter_talk_channel(self, sock: socket.socket, seq: sq.seqnum) -> NoReturn:
		self.talk_channel_open = True
		window = {}
			try:
				tasks = [
					self._send_packet( window, sock, seq ),
					self._recv( window, sock ),
					self._send_ack( sock ),
				]

				sock.gather( *tasks )
			except RuntimeError:
				raise
			
		# end of discussion
		sock.close()

	async def connect2friend(self, recvAddr: Tuple[str, int]) -> NoReturn:
		while True:
			(retsock, seq) = await self.initP2P( recvAddr )
			# might use try block later on
			if retsock is None:
				# wait for the function in ui to complete the yes/no part
				# for now, it always restart the routine
				print('remote end refused, wanna try again?')
				# user want to connect again
				raise NotImplementedError
			break
		
		# establish tcp socket
		(remote, _) = retsock.accpet()
		# since for now only a conversation is allowed
		# , we don not need to dispatch threads to handle socket
		# need threads to handle send and receive message

		# start to talk with friend
		await self._enter_talk_channel(remote, seq)


	def waiter(self) -> NoReturn:
		# local reference
		# following only accept IPv4 right now
		s = self.sock

		s.listen( self.blockTime )
		# accept calling
		clientsock, addr = s.accept()

		dataList = []
		while True:
			data = clientsock.rev(1024)
			if not data: break
			dataList.append[data]


		
		# channel ends
		clientsock.close()
		# might return dataList


	def callServer(self):
		s = self.sock 					# simplify the variable name
		s.connect( ( self.targetIP, self.targetPort ) )
		
		while True:						# break if 
			s.send( self.data )
			recv = s.recv(1024)			# receive stored at local
			if str(recv) == "¿" : break
			print( repr(recv) )
		
		# close socket