#!/usr/bin/env python3
from threading import RLock
from packet import notify
from typing import NoReturn

class seqnum():
	'''
	this class aim to keep track of the seqnum
	for each socket
	'''
	def __init__(self):
		self.num = 0
		self.rl = RLock()

	def getNum(self) -> int:
		rl.aquire()
		return self.num % 32

	def goNext(self) -> NoReturn:
		# it should not more than 1s for just increment a variable
		self.num += 1
		rl.release()
