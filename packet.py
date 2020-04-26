#!/usr/bin/env python3
from __future__ import print_function, annotations
from typing import NoReturn, Union, Optional,Type
from copy import copy, deepcopy
import sys
import struct

# got from the top answer of
# https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

class packet():
	SeqNumModulo = 32
	maxDatalength = 500

	__ShallPass = False

	def __init__(self, *args, magic=True):
		# prevent from being used publically
		assert(magic is packet.__ShallPass or packet.__ShallPass), \
			"packet objects must be created through create or copy methods"

		Type = args[0]
		Seqnum = args[1]
		Data = args[2]
		self.length = len(Data)
		if ( self.length > packet.maxDatalength ):
			eprint( Type, ",", Seqnum, ": data too large (max 500 chars)\n" )

		self.type = Type
		self.seqnum = Seqnum % packet.SeqNumModulo
		self.data = Data
		self.ACK = False

	def __copy__(self):
		cls = self.__class__
		result = cls.__new__(cls)
		result.__dict__.update(self.__dict__)
		return result

	def __deepcopy__(self, memo):
		'''
		below is sufficient enough for this class
		'''
		return type(self)(*self.__dict__.values())

	@classmethod
	def createACK(cls, Seqnum: int):
		return packet(0, Seqnum, "", magic=cls.__ShallPass)

	@classmethod
	def createPacket(cls, Seqnum: int, Data: str):
		return packet(1, Seqnum, Data, magic=cls.__ShallPass)

	@classmethod
	def createEOT(cls, Seqnum: int):
		return packet(2, Seqnum, "", magic=cls.__ShallPass)

	@classmethod
	def createConnRequest(cls, Seqnum: int, Data: str):
		return packet(3, Seqnum, Data, magic=cls.__ShallPass)

	# start to think that private constructor is not a thing for this class
	@classmethod
	def create(cls, Type: int, Seqnum: int, Data: str):
		return packet(Type, Seqnum, Data, magic=cls.__ShallPass)

	def getdata(self)-> bytes:
		fmt = '>iii{0}s'.format(self.length)
		packed = struct.pack(fmt, self.type, self.seqnum,
			self.length, self.data.encode("ASCII"))
		return packed

	@classmethod
	def parsedata(cls, data: bytes) -> packet:
		fmt = '>iii'
		retval = struct.unpack(fmt, data[:12])
		retdata = ""
		if (retval != 0):
			fmt = '>{0}s'.format(retval[2])
			retdata = struct.unpack(fmt, data[12:])

		return packet.create(retval[0], retval[1], retdata)

	def ACKrecv(self):
		self.ACK = True

	def check(self):
		assert(self.ACK), "ACK for this packet is still not received"