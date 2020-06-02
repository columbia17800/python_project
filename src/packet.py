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
	CONN:				login connection request contains (host, port)
	GET:				request to initialize P2P
	'''
	ACK, PACK, EOT, CONN, GET, REGISTER = range(6)

	def __init__(self, *args):
		self.type = args[0]
		self.data = args[1]
		self.length = args[2]
		self.spec = 0 if args[3] is None else args[3]
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

	def __repr__(self):
		return "{}{}{}{}{}{}".format(self.__class__, self.type,
			self.data, self.length, self.spec)

	@classmethod
	def createACK(cls, Data: Optional[str] = None, Spec: Optional[int] = None) -> packet:
		return cls(0, Data, 0 if Data is None else len(Data), Spec)

	@classmethod
	def createPacket(cls, Data: str, Spec: Optional[int] = None) -> packet:
		return cls(1, Data, len(Data), Spec)

	@classmethod
	def createEOT(cls, Data: Optional[str] = None, Spec: Optional[int] = None) -> packet:
		return cls(2, Data, 0 if Data is None else len(Data), Spec)

	@classmethod
	def createConnRequest(cls, Data: str, Spec: Optional[int] = None) -> packet:
		return cls(3, Data, len(Data), Spec)

	@classmethod
	def createGet(cls, Data: str, Spec: Optional[int] = None) -> packet:
		return cls(4, Data, len(Data), Spec)

	@classmethod
	def createRegister(cls, Data: str, Spec: Optional[int] = None) -> packet:
		return cls(5, Data, len(Data), Spec)

	def getdata(self)-> bytes:
		fmt = '>iii'
		packed = struct.pack(fmt, self.type,
			self.length, self.spec)
		if self.data is not None:
			packed += self.data.encode("UTF-8")
		return packed

	@classmethod
	def parsedata(cls, data: bytes) -> packet:
		fmt = '>iii'
		retval = struct.unpack(fmt, data[:12])
		retdata = None
		if len(data) > 12:
			retdata = data[12:].decode("UTF-8")

		return cls(retval[0], retdata, retval[1], retval[2])