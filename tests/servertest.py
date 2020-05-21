#!/usr/bin/env python3
import sys
import os.path as path
sys.path.append( path.dirname(path.dirname(path.abspath(__file__))) )

from src.utility import recv_tcp, send_tcp
from src.packet import packet
import unittest
import socket

class testserver(unittest.TestCase):
	def _create_connection(self):
		return socket.create_connection(("localhost", 9999))

	def test_ack(self):
		pass

	def test_pack(self):
		client = self._create_connection()
		p = packet.createPacket(0, "Hello World!")
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		client.close()
		self.assertEqual(retp.type , packet.ACK)

	def test_register(self):
		client = self._create_connection()
		p = packet.createRegister(0, str(("dibs", "123321")))
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		client.close()
		self.assertEqual(retp.type , packet.ACK)

	def test_register_and_get(self):
		client = self._create_connection()
		p = packet.createRegister(0, str(("Dibs", "123321")))
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		self.assertEqual(retp.type , packet.ACK)

		p = packet.createConnRequest(0, str(("Dibs", "123321")))
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		self.assertEqual(retp.type , packet.ACK)

		p = packet.createGet(0, "Dibs")
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )

		client.close()
		self.assertEqual(retp.type , packet.ACK)

	def test_registed_same_usr(self):
		client = self._create_connection()
		p = packet.createRegister(0, str(("another", )))
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		client.close()
		self.assertEqual(retp.type , packet.EOT)
		self.assertEqual(retp.data, "write your password in the field")

	def test_registed_attempt(self):
		client = self._create_connection()
		p = packet.createRegister(0, str(("Newbee", "123321")))
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		self.assertEqual(retp.type, packet.ACK)

		p = packet.createRegister(0, str(("Newbee", "123321")))
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		client.close()
		self.assertEqual(retp.type , packet.EOT)
		self.assertEqual(retp.data, "selected name is registered")

	def test_get(self):
		pass

	def test_conn(self):
		pass

	def test_eot(self):
		client = self._create_connection()
		p = packet.createEOT(0)
		ret = client.sendall(p.getdata())
		retp = recv_tcp( client )
		client.close()
		self.assertEqual(retp.type , packet.EOT)

if __name__ == '__main__':
	unittest.main()