import struct
from GAFpy.utils import readU32, readU16, readU8, readFloat, readString, readVec, readColor, readAffineTransform, readRect
#import GAFpy.Parser

def readTag(inStream, parent, context):
	tagId = readU16(inStream)
	#print("TagId = {0}".format(tagId))
	tag = Tag(context)
	try:
		tag = TagList[tagId](context)
		print type(tag)
	except KeyError:
		print("GAF format warning. Unknonwn tag with number {0}".format(tagId))
	tag.parse(inStream)
	parent.append({'name': tag.type(), 'content': tag.data})
	return tag

class Tag(object):
	_context = object()
	_data = {}

	@property
	def data(self):
		return self._data

	"""Base class for GAF tags"""
	def __init__(self, context):
		self._data = {}
		self._context = context

	def parse(self, inStream):
		length = readU32(inStream)
		self.doParse(inStream, length)

	def doParse(self, inStream, length):
		#print("Tag length is {0}".format(length))
		inStream.read(length)

	def type(self):
		if type(self) is Tag:
			return 'Unknonw'
		else:
			return type(self).__name__

	def header(self):
		return self._context['header']

	def version(self):
		return self.header()['majorVersion']

	def tagInContext(self, tag):
		tags = self._context['tags']
		match = [x for x in tags if x['name'] == tag]
		return match

class TagEnd(Tag):
	"""Final tag"""
	def __init__(self, context):
		Tag.__init__(self, context)

	def parse(self, inStream):
		return

class TagDefineAtlas(Tag):
	"""All used atlases in animation"""
	def __init__(self, context):
		Tag.__init__(self, context)
		
	def doParse(self, inStream, length):
		c = self._data
		scale = readFloat(inStream)
		c['scale'] = scale
		atlasesCount = readU8(inStream)
		c['atlasesCount'] = atlasesCount
		atlases = []
		for i in range(0, atlasesCount):
			atlas = {}
			atlasId = readU32(inStream)
			atlas['atlasId'] = atlasId
			sources = readU8(inStream)
			atlas['atlasSourcesCount'] = sources
			atlas['atlasSources'] = []
			for i in range(0, sources):
				atlasSource = {}
				fileName = readString(inStream)
				atlasSource['fileName'] = fileName
				csf = readFloat(inStream)
				atlasSource['CSF'] = csf
				atlas['atlasSources'].append(atlasSource)
			atlases.append(atlas)
		c['atlases'] = atlases

		elements = []
		elementsCount = readU32(inStream)
		for i in range(0, elementsCount):
			element = {}
			element['pivot'] = readVec(inStream)
			element['origin'] = readVec(inStream)
			
			element['scale'] = readFloat(inStream)

			element['width'] = readFloat(inStream)
			element['height'] = readFloat(inStream)

			atlasIndex = readU32(inStream)
			if atlasIndex > 0:
				atlasIndex -= 1
			element['atlasIndex'] = atlasIndex

			elementAtlasIndex = readU32(inStream)
			element['elementAtlasIndex'] = elementAtlasIndex

			if self.version() >= 4:
				hasScale9Grid = readU8(inStream)
				element['hasScale9Grid'] = hasScale9Grid
				if hasScale9Grid:
					# scale9GridRect
					element['scale9Grid'] = readRect(inStream)

			elements.append(element)
		c['elements'] = elements



		self._data = c

class TagDefineAnimationMasks(Tag):
	"""xxx"""
	def __init__(self, context):
		Tag.__init__(self, context)
	
class TagDefineAnimationObjects(Tag):
	"""Objects in animation"""
	def __init__(self, context):
		Tag.__init__(self, context)

	def doParse(self, inStream, length):
		c = self._data
		count = readU32(inStream)
		c["objectsCount"] = count
		objects = []
		while count:
			obj = {}
			objectId = readU32(inStream)
			obj["id"] = objectId
			atlasIdRef = readU32(inStream)
			obj['atlasIdRef'] = atlasIdRef
			if self.version() >= 4:
				objType = readU16(inStream)
				obj['type'] = objType
			objects.append(obj)
			count -= 1
		c["objects"] = objects
		self._data = c
	
class TagDefineAnimationFrames(Tag):
	"""Each frame state"""

	GFT_DropShadow = 0
	GFT_Blur = 1
	GFT_Glow = 2
	GFT_ColorMatrix = 6

	def __init__(self, context):
		Tag.__init__(self, context)

	def doParse(self, inStream, length):
		startPos = inStream.tell()
		c = self._data
		c['states'] = []
		animationObjects = self.tagInContext('TagDefineAnimationObjects')[0]['content']['objects']
		readU32(inStream) # read count. Unused here
		totalFrames = self.header()['frameCount']
		frameNumber = readU32(inStream)
		for i in range(0, totalFrames):
			frame = []
			currentStates = {}
			frameState = {}
			if (frameNumber - 1) == i:
				objectsCount = readU32(inStream)
				stateList = []
				for obj in range(0, objectsCount):
					state = self.extractState(inStream)
					stateList.append(state)
				for st in stateList:
					currentStates[st['objectIdRef']] = st
				if startPos + length > inStream.tell():
					frameNumber = readU32(inStream)
				c['states'].append(currentStates)

			#states[]
		self._data = c


	def extractState(self, inStream):
		state = {}
		hasColorTransform = readU8(inStream)
		hasMasks = readU8(inStream)
		hasEffect = readU8(inStream)
		state['objectIdRef'] = readU32(inStream)
		state['zIndex'] = readU32(inStream)
		state['colorOffsets'] = {}
		state['colorMults'] = {'a' :readFloat(inStream)}
		state['affineTransform'] = readAffineTransform(inStream)
		if hasColorTransform:
			state['colorOffsets']['a'] = readFloat(inStream)
			state['colorMults']['r'] = readFloat(inStream)
			state['colorOffsets']['r'] = readFloat(inStream)
			state['colorMults']['g'] = readFloat(inStream)
			state['colorOffsets']['g'] = readFloat(inStream)
			state['colorMults']['b'] = readFloat(inStream)
			state['colorOffsets']['b'] = readFloat(inStream)
		else:			
			state['colorOffsets']['a'] = 0
			state['colorMults']['r'] = 1
			state['colorOffsets']['r'] = 0
			state['colorMults']['g'] = 1
			state['colorOffsets']['g'] = 0
			state['colorMults']['b'] = 1
			state['colorOffsets']['b'] = 0

		if hasEffect:
			state['effects'] = []
			effects = readU8(inStream)
			for e in range(0, effects):
				filterType = readU32(inStream)
				filt = {'type' : 'none'}
				if filterType == self.GFT_Blur:
					filt['type'] = 'blur'
					filt['blurSize'] = readVec(inStream)					
				elif filt == self.GFT_Glow:
					filt['type'] = 'glow'
					filt['color'] = readColor(inStream)
					filt['blurSize'] = readVec(inStream)
					filt['strength'] = readFloat(inStream)
					filt['innerGlow'] = bool(readU8(inStream))
					filt['knockout'] = bool(readU8(inStream))
				elif filt == self.GFT_DropShadow:
					filt['type'] = 'dropShadow'
					filt['color'] = readColor(inStream)
					filt['angle'] = readFloat(inStream)
					filt['distance'] = readFloat(inStream)
					filt['strength'] = readFloat(inStream)
					filt['innerShadow'] = readFloat(inStream)
					filt['knockout'] = readFloat(inStream)
				state['effects'].append(filt)

		if hasMasks:
			state['maskObjectIdRef'] = readU32(inStream)
		return state

class TagDefineNamedParts(Tag):
	"""xxx"""
	def __init__(self, context):
		Tag.__init__(self, context)
	
class TagDefineSequences(Tag):
	"""xxx"""
	def __init__(self, context):
		Tag.__init__(self, context)

class TagDefineTextFields(Tag):
	"""xxx"""
	def __init__(self, context):
		Tag.__init__(self, context)

class TagDefineStage(Tag):
	"""General information for stage"""
	def __init__(self, context):
		Tag.__init__(self, context)

	def doParse(self, inStream, length):
		self.data['fps'] = readU8(inStream)
		self.data['color'] = readColor(inStream)
		self.data['width'] = readU16(inStream)
		self.data['height'] = readU16(inStream)
    
class TagDefineAnimationFrames2(Tag):
	"""xxx"""
	def __init__(self, context):
		Tag.__init__(self, context)

class TagDefineTimeline(Tag):
	"""Timeline tag. Since v4.0"""
	def __init__(self, context):
		Tag.__init__(self, context)

	def doParse(self, inStream, length):
		readU32(inStream)
		readU32(inStream)
		aabb = readRect(inStream)
		pivot = readVec(inStream)
		self.header()['pivot'] = pivot
		self.header()['frameSize'] = aabb
		hasLinkage = readU8(inStream)
		if hasLinkage:
			linkageName = readString(inStream)
		d = []
		readTag(inStream, d, self._context)
		self._data['timelines'] = d

TagList = {
0: TagEnd,
1: TagDefineAtlas,
2: TagDefineAnimationMasks,
3: TagDefineAnimationObjects,
4: TagDefineAnimationFrames,
5: TagDefineNamedParts,
6: TagDefineSequences,
7: TagDefineTextFields,
8: TagDefineAtlas,
9: TagDefineStage,
11: TagDefineAnimationMasks,
10: TagDefineAnimationObjects,
12: TagDefineAnimationFrames2,
13: TagDefineTimeline}

