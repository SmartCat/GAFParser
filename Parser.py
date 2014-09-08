from GAFpy import Tags
from GAFpy.utils import readU32, readU16, readU8, readFloat, readString, readVec, readRect


class Parser:
	_context = {}

	def __init__(self):
		self._context = {}
		
	def result(self):
		return self._context

	def parse(self, inStream):
		self.readHeader(inStream)
		self._context["tags"] = []

		lastTag = Tags.Tag(self)
		while type(lastTag) is not Tags.TagEnd:
			lastTag = Tags.readTag(inStream, self._context["tags"], self._context)



	def readHeader(self, inStream):
		footprint = readU32(inStream)
		valid = (footprint == 0x00474146) or (footprint == 0x00474143)
		compressed = (footprint == 0x00474143)


		majorVersion = readU8(inStream)
		minorVersion = readU8(inStream)
		print("GAF v{0}.{1}".format(majorVersion, minorVersion))
		fileLength = readU32(inStream)

		h = {}
		h['valid'] = valid
		h['compressed'] = compressed
		h['majorVersion'] = majorVersion
		h['minorVersion'] = minorVersion

		self._context['header'] = h
		if(majorVersion < 4):
			self.readHeaderEndV3(inStream)
		else:
			self.readHeaderEndV4(inStream)


	def readHeaderEndV3(self, inStream):
		frameCount = readU16(inStream)
		frameSize = readRect(inStream)
		pivot = readVec(inStream)

		h = self._context['header']
		h['frameCount'] = frameCount
		h['frameSize'] = frameSize
		h['pivot'] = pivot
		self._context['header'] = h

	def readHeaderEndV4(self, inStream):
		h = self._context['header']

		scaleValuesCount = readU32(inStream)		
		h['scaleValuesCount'] = scaleValuesCount
		scaleValues = []
		#print("scaleValuesCount = {0}".format(scaleValuesCount))
		while scaleValuesCount != 0:
			scaleValues.append(readFloat(inStream))
			scaleValuesCount -= 1
		h['scaleValues'] = scaleValues

		CSFValuesCount = readU32(inStream)
		CSFValues = []
		#print("CSFValuesCount = {0}".format(CSFValuesCount))
		h['CSFValuesCount'] = CSFValuesCount
		while CSFValuesCount != 0:
			CSFValues.append(readFloat(inStream))
			CSFValuesCount -= 1
		h['CSFValues'] = CSFValues
		
		self._context['header'] = h
		