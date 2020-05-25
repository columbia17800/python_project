#!usr/bin/env python3
import sys
import os.path as path
sys.path.append( path.dirname(path.dirname(path.abspath(__file__))) )

from src.loginui import LogUI
import unittest

class logintest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.login = LogUI()

	def test_eventloop(self):
		self.login.eventloop()

if __name__ == '__main__':
	unittest.main()
