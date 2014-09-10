"""Package 
"""
from GAFpy.Parser import Parser

def load(file):
	try:
		f = open(file, 'rb')
	finally:
		p = Parser()
		p.parse(f)
		f.close()
		return p.result()

def findTags(gaf, tag):
	_gaf = gaf
	if type(_gaf) is dict and 'tags' in _gaf.keys():
		_gaf = gaf['tags']
	return [a for a in _gaf if a['name'] == tag]
