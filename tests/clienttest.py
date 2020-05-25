#!/usr/bin/env python3
import sys
import os.path as path
sys.path.append( path.dirname(path.dirname(path.abspath(__file__))) )

from src.client import Client, registrationError
import unittest
import socket
import time

class testclient(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.client = Client()
		self.client.start()
		self.client.runningloop.wait()
	
	@classmethod
	def tearDownClass(self):
		self.client.stop()
	
	def test_register(self):
		try:
			self.client.register(('dibs', '123'))
		except registrationError as re:
			print(re.reason)

	def test_conn(self):
		try:
			self.client.register(('sumbitch', 'sumpassword'))

			self.client.connect_to_server(('sumbitch', 'sumpassword'))
		except:
			raise

if __name__ == '__main__':
	unittest.main()