#!/usr/bin/env python3
import socket
from packet import packet
from typing import NoReturn, Union,Optional
import seqnum as sq
import asyncio
from utility import send_tcp, recv_tcp

class Chatter():
	#""A simple TCP/UDP chat""
	
	def __init__(self):
		# create the first socket that communicate with main server
		Host = ''				# not known yet
		Port = 80				# through http port
		self.mainAddr = ( Host, Port )
		self.window = {}				# window used for storing packets
		self.task_window = {}
		self.seqnum = sq.seqnum()
		self.talk_channel_open = False
		self.msg = []
		self.recv_msg = []
		self.base = 0
		self.notifing_packet = []
		self.notify = async.Event()
		self.msg_signal = async.Event()

	def __del__(self):
		self.mainSock.close()

	async def _create_n_update_packet(self, packet_type: int, data=None) -> Tuple[packet, int]:
		seqnum = self.seqnum.getNum()
		p = packet(packet_type, seqnum, data,
			0 if data is None else len(data))

		while self.window.get(seqnum) is not None:
			await asyncio.sleep( 1 )

		self.window[seqnum] = p
		self.seqnum.goNext()
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
	async def initP2P( self, target:Tuple[str, int] ) -> Optional[socket.socket]:
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
			(p, sqnum) = await self._create_n_update_packet( packet.CONN, str(addr) )
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
				self.window[sqnum] = None
				return None
			elif rettype == packet.ACK:
				self.window[sqnum] = None
				sock.listen(1)
				return sock
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
		
		(p, sqnum) = await self._create_n_update_packet( packet.GET )

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

		(p, sqnum) = await self._create_n_update_packet( packet.GET, name )
		
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
	async def _send_packet(self, sock: socket.socket) -> NoReturn:
		while self.talk_channel_open:
			await self.msg_signal.wait():

				msg = self.msg.popleft()

				(p, sqnum) = await self._create_n_update_packet( packet.PACK, msg )
				send_tcp( sock, p.getdata() )

				task = asyncio.create_task(self._time_out(sock, sqnum))

				if self.task_window[sqnum]:
					self.task_window[sqnum].cancel()
				self.task_window[sqnum] = task
				
				if msg.count() is 0:
					self.msg_signal.clear()

	async def _time_out(self, sock: socket.socket, seqnum: int) -> NoReturn:
		try:
			while self.talk_channel_open:
				await asyncio.sleep( 60 )
				# ignore that packet might send due to race condition
				p = self.window[seqnum]
				if p is None:
					break
				send_tcp( sock, p.getdata() )
		except asyncio.CancelledError:
			print('Wasted {}', seqnum)
			pass
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

	async def _send_ack(self, sock: socket.socket) -> NoReturn:
		while self.talk_channel_open:
			# ack packets are not counting and storing in window
			await self.notify.wait()
			
			seq = self.notifing_packet.popleft()

			p = packet.createACK( seq )

			sock.sendall( p.getdata() )

			if self.notifing_packet.count() is 0:
				self.notify.clear()

	async def _recv(self, sock:socket.socket) -> NoReturn:
		while self.talk_channel_open:
			ret = recv_tcp(sock)
			rettype = ret.type

			if rettype == packet.ACK:
				self.window[ret.seqnum] = None
			elif rettype == packet.PACK:
				# received packet and send back ack packet to notify sender
				self.recv_msg.append( ret.data )
				
				self.notifing_packet.append( ret.seqnum )

				with self.notify as notify:
				# set notify to get _send_ack called
					if !notify.is_set():
						notify.set()

			elif rettype == packet.EOT:
				self.talk_channel_open = False
			else:
				raise NotImplementedError

	# for now, only one socket is used for discussion
	# don't know it will or not lead to race condition on send or recv
	# wait until it is testified 
	# to decide how many sockets the channel needs
	async def _enter_talk_channel(self, sock: socket.socket) -> NoReturn:
		self.talk_channel_open = True
			try:
				task = []

				task.append(asyncio.create_task( self._send_packet( sock ) ))
				task.append(asyncio.create_task( self._recv( sock ) ))
				task.append(asyncio.create_task( self._send_ack( sock ) ))

				sock.gather( *task )
			except RuntimeError:
				raise
			
		# end of discussion
		sock.close()

	async def connect2friend(self, recvAddr: Tuple[str, int]) -> NoReturn:
		while True:
			retsock = await self.initP2P( recvAddr )
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
		await self._enter_talk_channel(remote)


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