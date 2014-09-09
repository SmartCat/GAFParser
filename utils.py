import struct

def readU32(s):
	return struct.unpack("<I", s.read(4))[0]

def readS32(s):
	return struct.unpack("<i", s.read(4))[0]

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

def readAffineTransform(s):
	ret = {}
	ret['a'] = readFloat(s)
	ret['b'] = readFloat(s)
	ret['c'] = readFloat(s)
	ret['d'] = readFloat(s)
	ret['tx'] = readFloat(s)
	ret['ty'] = readFloat(s)
	return ret


def readColor(s):
	ret = {}
	ret['r'] = readU8(s)
	ret['g'] = readU8(s)
	ret['b'] = readU8(s)
	ret['a'] = readU8(s)
	return ret