#!/usr/bin/env python3
from threading import Timer
from packet import notify

class seqnum():
	'''
	this class aim to keep track of the seqnum
	for each socket
	'''
	def __init__(self):
		self.num = 0

	def getNum():
		return num

	def getNext():
		return num++

	def setTimer(Seqnum: int):
		t = Timer( 60.0, notify, Seqnum )
		t.start()