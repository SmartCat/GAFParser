""" Package for parsing GAF files

Returns dictionary of header and tags in GAF

import GAFParser, os

gafFiles = [a for a in os.listdir('.') if os.path.isfile(a) and os.path.splitext(a)[1] == '.gaf']
for f in gafFiles:
	g = GAFParser.load(f)
	majorVersion = g['header']['majorVersion']
	minorVersion = g['header']['minorVersion']
	compressed = g['header']['compressed']
	print("GAF v{0}.{1} \tCompressed {2}".format(majorVersion, minorVersion, compressed))


"""
import Parser

def load(file):
	try:
		f = open(file, 'rb')
	finally:
		p = Parser.Parser()
		p.parse(f)
		f.close()
		return p.result()

def findTags(gaf, tag):
	_gaf = gaf
	if type(_gaf) is dict and 'tags' in _gaf.keys():
		_gaf = gaf['tags']
	return [a for a in _gaf if a['name'] == tag]
