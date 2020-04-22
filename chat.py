import socket

class Chatter():
	""A simple TCP/UDP chat""
	
	def __init__(self, targetIP, targetPort, selfIP, selfPort):
		self.targetIP = targetIP
		self.targetPort = targetPort
		self.selfIP = selfIP
		self.selfPort = self.selfPort
		self.blockTime = 1
		self.sock = socket.socket(
			socket.AF_INET, 
			socket.SOCK_STREAM)

	def __del__(self):
		closeSocket()

	def initialTunnel(self):
		# local reference
		# following only accept IPv4
		s = self.sock
		s.bind( ( self.selfIP, self.selfPort ) )
		s.listen( self.blockTime )
		# accept calling
		conn, addr = s.accept()

		dataList = []
		while True:
			data = conn.rev(1024)
			if not data: break
			dataList.append[data]
		
		# channel ends
		conn.close()
		# might return dataList


	def callServer(self):
		s = self.socket
		s.connect( ( self.targetIP, self.targetPort ) )
		
		while True:						# break if 
			s.send( self.data )
			recv = s.recv(1024)			# receive stored at local
			if str(recv) = "¿" : break
			print repr(recv)
		
		closeSocket(self)						# close socket


	def closeSocket(self):
		s.close()