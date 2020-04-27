#!/usr/bin/env python3
from threading import Timer, RLock, current_thread
from packet import notify
from typing import NoReturn

class my_timer(Timer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.exc = None
		self.parent = current_thread()

	def run(self):
		try:
			super().run()
		except Exception as e:
			self.exc = e

class seqnum():
	'''
	this class aim to keep track of the seqnum
	for each socket
	'''
	def __init__(self):
		self.num = 0
		self.rl = RLock()

	def getNum(self) -> int:
		return self.num

	def goNext(self) -> NoReturn:
		# it should not more than 1s for just increment a variable
		with rl:
			self.num += 1

	def setTimer(self, Seqnum: int) -> NoReturn:
		self.t = Timer( 60.0, notify, Seqnum )
		
	def start(self) -> NoReturn:
		# this is trivial
		if self.exc:
			raise self.exc
		t.start()
