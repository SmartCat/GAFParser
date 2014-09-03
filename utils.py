import struct

def readU32(s):
	return struct.unpack("<I", s.read(4))[0]

def readU16(s):
	return struct.unpack("<H", s.read(2))[0]

def readU8(s):
	return struct.unpack("<B", s.read(1))[0]

def readFloat(s):
	return struct.unpack("<f", s.read(4))[0]

def readString(s):
	len = readU16(s)
	fmt = "<{0}s".format(len)
	return struct.unpack(fmt, s.read(len))[0]

def readVec(s):
	ret = {}
	ret['x'] = readFloat(s)
	ret['y'] = readFloat(s)
	return ret

def readRect(s):
	ret = {}
	ret['pos'] = readVec(s)
	ret['size'] = readVec(s)
	return ret
