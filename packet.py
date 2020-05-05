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
	maxDatalength = 500
	'''
	Below is the type of packet
	ACK:				received (Acknowledgement from receiver to sender)
	EOT:				close or end of communication
	PACK:				data string packet
	CONN:				connection request contains (host, port)
	GET:				request to get the (host, port) pair from server
	'''
	ACK, PACK, EOT, CONN, GET, REGISTER = range(6)

	def __init__(self, *args, ver: Optional[bool] = None):
		self.type = args[0]
		self.seqnum = args[1]
		self.data = args[2]
		self.length = args[3]
		self.version = 1 if ver else 0
		# no limit on length

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
	def createACK(cls, Seqnum: int, Data: Optional[str] = None, ver: Optional[bool] = None) -> packet:
		return cls(0, Seqnum, Data, 0 if Data is None else len(Data), 1 if ver else 0)

	@classmethod
	def createPacket(cls, Seqnum: int, Data: str, ver: Optional[bool] = None) -> packet:
		return cls(1, Seqnum, Data, len(Data), 1 if ver else 0)

	@classmethod
	def createEOT(cls, Seqnum: int, Data: str = None, ver: Optional[bool] = None) -> packet:
		return cls(2, Seqnum, Data, 0 if Data is None else len(Data), 1 if ver else 0)

	@classmethod
	def createConnRequest(cls, Seqnum: int, Data: str, ver: Optional[bool] = None) -> packet:
		return cls(3, Seqnum, Data, len(Data), 1 if ver else 0)

	@classmethod
	def createGet(cls, Seqnum: int, Data: str, ver: Optional[bool] = None) -> packet:
		return cls(4, Seqnum, Data, len(Data), 1 if ver else 0)

	@classmethod
	def createRegister(cls, Seqnum: int, Data: str, ver: Optional[bool] = None) -> packet:
		return cls(5, Seqnum, Data, len(Data), 1 if ver else 0)

	def getdata(self)-> bytes:
		fmt = '>?iii'
		packed = struct.pack(fmt, self.version, self.type, self.seqnum,
			self.length)
		if self.data is not None:
			packed += self.data.encode("UTF-8")
		return packed

	@classmethod
	def parsedata(cls, data: bytes) -> packet:
		fmt = '>?iii'
		retval = struct.unpack(fmt, data[:13])
		retdata = None
		if len(data) > 13:
			retdata = data[13:].decode("UTF-8")

		return cls(retval[1], retval[2], retdata, retval[3], retval[0])