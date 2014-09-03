import struct
from GAFpy.utils import readU32, readU16, readU8, readFloat, readString
#import GAFpy.Parser

class TagUnknown(object):
	context = object()
	data = {}
	"""Base class for GAF tags"""
	def __init__(self, context):
		self.context = context

	def parse(self, inStream):
		length = readU32(inStream)
		self.doParse(inStream, length)

	def doParse(self, inStream, length):
		#print("TagUnknown length is {0}".format(length))
		inStream.read(length)

	def getData(self):
		return {'type': self.type(), 'content': self.data}

	def type(self):
		return type(self).__name__

	def _getData(self):
		return {'type': 'Unknown', 'content': {}}

class TagEnd(TagUnknown):
	"""Final tag"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

	def parse(self, inStream):
		return

class TagDefineAtlas(TagUnknown):
	"""All used atlases in animation"""

	content = {}

	def __init__(self, context):
		TagUnknown.__init__(self, context)
		self.content['type'] = self.type()
		self.content['content'] = {}
		
	def doParse(self, inStream, length):
		c = self.content['content']
		scale = readFloat(inStream)
		c['scale'] = scale
		atlasesCount = readU8(inStream)
		c['atlasesCount'] = atlasesCount
		atlases = []
		while atlasesCount:
			atlas = {}
			atlasId = readU32(inStream)
			atlas['atlasId'] = atlasId
			sources = readU8(inStream)
			atlas['atlasSourcesCount'] = sources
			atlas['atlasSources'] = []
			while sources:
				atlasSource = {}
				fileName = readString(inStream)
				atlasSource['fileName'] = fileName
				csf = readFloat(inStream)
				atlasSource['CSF'] = csf
				atlas['atlasSources'].append(atlasSource)
				sources -= 1
			atlasesCount -= 1
			atlases.append(atlas)
		c['atlases'] = atlases

		elementsCount = readU32(inStream)
		while elementsCount:
			# pivot
			readFloat(inStream)
			readFloat(inStream)
			# origin
			readFloat(inStream)
			readFloat(inStream)
			
			scale = readFloat(inStream)

			width = readFloat(inStream)
			height = readFloat(inStream)

			atlasIndex = readU32(inStream) - 1
			if atlasIndex < 0:
				atlasIndex + 1

			elementAtlasIndex = readU32(inStream)

			version = self.context['header']['majorVersion']
			if version >= 4:
				hasScale9Grid = readU8(inStream)
				if hasScale9Grid:
					# scale9GridRect
					readFloat(inStream)
					readFloat(inStream)
					readFloat(inStream)
					readFloat(inStream)



			elementsCount -= 1
		self.content["content"] = c

	def getData(self):
		return self.content

class TagDefineAnimationMasks(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)
		

class TagDefineAnimationObjects(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)
		

class TagDefineAnimationFrames(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)
		

class TagDefineNamedParts(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)
		

class TagDefineSequences(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineTextFields(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineAtlas2(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineStage(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineAnimationMasks2(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineAnimationObjects2(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineAnimationFrames2(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)

class TagDefineTimeline(TagUnknown):
	"""xxx"""
	def __init__(self, context):
		TagUnknown.__init__(self, context)


TagList = {
0: TagEnd,
1: TagDefineAtlas,
2: TagDefineAnimationMasks,
3: TagDefineAnimationObjects,
4: TagDefineAnimationFrames,
5: TagDefineNamedParts,
6: TagDefineSequences,
7: TagDefineTextFields,
8: TagDefineAtlas2,
9: TagDefineStage,
11: TagDefineAnimationMasks2,
10: TagDefineAnimationObjects2,
12: TagDefineAnimationFrames2,
13: TagDefineTimeline}

