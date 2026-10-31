import struct

import numpy as np


class ByteStream:
	def __init__(self, buffer=b"", endian="little", stringLengthSize=2):
		self.buffer = bytearray(buffer)
		self.endian = endian
		self.stringLengthSize = stringLengthSize
		
		self.offset = 0
	
	@property
	def endianSign(self):
		return ">" if self.endian == "big" else "<"
	
	def isAtEnd(self):
		return self.offset >= len(self.buffer)
	
	def align(self, value, padValue=None):
		length = -self.offset % value
		if padValue is None:
			self.offset += length
		else:
			self.writeBytes(bytes((padValue,)) * length)
		
		return length
	
	def readBytes(self, size):
		size = max(size, 0)
		
		if self.offset + size > len(self.buffer):
			raise EOFError("Not enough bytes to read")
		
		result = self.buffer[self.offset:self.offset + size]
		self.offset += size
		
		return result

	def readSizedBytes(self):
		return self.readBytes(self.readUInt32())
	
	def readInt(self, size):
		return int.from_bytes(self.readBytes(size), self.endian, signed=True)
	
	def readUInt(self, size):
		return int.from_bytes(self.readBytes(size), self.endian)
	
	def readInt8(self):
		return self.readInt(1)
	
	def readUInt8(self):
		return self.readUInt(1)
	
	def readInt16(self):
		return self.readInt(2)
	
	def readUInt16(self):
		return self.readUInt(2)
	
	def readInt24(self):
		return self.readInt(3)
	
	def readUInt24(self):
		return self.readUInt(3)
	
	def readInt32(self):
		return self.readInt(4)
	
	def readUInt32(self):
		return self.readUInt(4)
	
	def readInt64(self):
		return self.readInt(8)
	
	def readUInt64(self):
		return self.readUInt(8)
	
	def readFloat32(self):
		return struct.unpack(self.endianSign + "f", self.readBytes(4))[0]
	
	def readFloat64(self):
		return struct.unpack(self.endianSign + "d", self.readBytes(8))[0]
	
	def readBoolean(self):
		return bool(self.readUInt8())
	
	def readRawString(self, length):
		return self.readBytes(length).decode()
	
	def readString(self):
		return self.readRawString(self.readUInt(self.stringLengthSize))
	
	def readCString(self):
		try:
			endOffset = self.buffer.index(0, self.offset)
		except ValueError:
			raise ValueError("End terminator not found") from None
		result = self.readRawString(endOffset - self.offset)
		self.offset += 1

		return result
	
	def readLEB128(self):
		result = 0
		shift = 0
		while True:
			byte = self.readUInt8()
			result |= (byte & 0x7F) << shift
			shift += 7
			if not (byte & 0x80):
				if byte & 0x40:
					result -= 1 << shift
				break
		
		return result
	
	def readULEB128(self):
		result = 0
		shift = 0
		while True:
			byte = self.readUInt8()
			result |= (byte & 0x7F) << shift
			shift += 7
			if not (byte & 0x80):
				break
		
		return result
	
	def readMatrix(self, rowMajor=False):
		matrixDataType = np.dtype(self.endianSign + "f4")
		matrix = np.frombuffer(self.readBytes(4 * 4 * matrixDataType.itemsize), matrixDataType).reshape(4, 4)
		return matrix.transpose() if rowMajor else matrix
	
	def writeBytes(self, value):
		size = len(value)
		self.buffer[self.offset:self.offset + size] = value
		self.offset += size
		return value

	def writeSizedBytes(self, value):
		self.writeUInt32(len(value))
		return self.writeBytes(value)
	
	def writeInt(self, value, size):
		self.writeBytes(value.to_bytes(size, self.endian, signed=True))
		return value
	
	def writeUInt(self, value, size):
		self.writeBytes(value.to_bytes(size, self.endian))
		return value
	
	def writeInt8(self, value):
		return self.writeInt(value, 1)
	
	def writeUInt8(self, value):
		return self.writeUInt(value, 1)
	
	def writeInt16(self, value):
		return self.writeInt(value, 2)
	
	def writeUInt16(self, value):
		return self.writeUInt(value, 2)
	
	def writeInt24(self, value):
		return self.writeInt(value, 3)
	
	def writeUInt24(self, value):
		return self.writeUInt(value, 3)
	
	def writeInt32(self, value):
		return self.writeInt(value, 4)
	
	def writeUInt32(self, value):
		return self.writeUInt(value, 4)
	
	def writeInt64(self, value):
		return self.writeInt(value, 8)
	
	def writeUInt64(self, value):
		return self.writeUInt(value, 8)
	
	def writeFloat32(self, value):
		self.writeBytes(struct.pack(self.endianSign + "f", value))
		return value
	
	def writeFloat64(self, value):
		self.writeBytes(struct.pack(self.endianSign + "d", value))
		return value
	
	def writeBoolean(self, value):
		self.writeUInt8(1 if value else 0)
		return value
	
	def writeRawString(self, value):
		self.writeBytes(value.encode())
		return value
	
	def writeString(self, value):
		self.writeUInt(len(value.encode()), self.stringLengthSize)
		return self.writeRawString(value)
	
	def writeCString(self, value):
		self.writeRawString(value)
		self.writeUInt8(0)
		return value
	
	def writeLEB128(self, value):
		tempValue = value
		while True:
			byte = tempValue & 0x7F
			tempValue >>= 7
			if (tempValue == 0 and byte & 0x40 == 0) or (tempValue == -1 and byte & 0x40 != 0):
				self.writeUInt8(byte)
				break
			else:
				self.writeUInt8(byte | 0x80)
		
		return value
	
	def writeULEB128(self, value):
		tempValue = value
		while True:
			byte = tempValue & 0x7F
			tempValue >>= 7
			if not tempValue:
				self.writeUInt8(byte)
				break
			else:
				self.writeUInt8(byte | 0x80)
		
		return value
	
	def writeMatrix(self, matrix, rowMajor=False):
		if rowMajor:
			matrix = matrix.transpose()
		self.writeBytes(matrix.astype(self.endianSign + "f4", copy=False).tobytes())
		
		return matrix