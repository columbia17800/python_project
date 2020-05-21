#!/usr/bin/env python3
from threading import RLock
from typing import NoReturn,Tuple

class seqnum():
	'''
	this class aim to keep track of the seqnum
	for each socket
	'''
	def __init__(self):
		self.num = 0
		self.rl = RLock()

	def getNum(self) -> Tuple[int, bool]:
		self.rl.acquire()
		return (self.num % 32, (bool)(self.num / 32) % 2)

	def goNext(self) -> NoReturn:
		# it should not more than 1s for just increment a variable
		self.num += 1
		self.rl.release()
