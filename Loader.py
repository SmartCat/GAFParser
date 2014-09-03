from GAFpy.Parser import Parser

def load(file):
	try:
		f = open(file, 'rb')
	finally:
		p = Parser()
		p.parse(f)
		f.close()
		return p.result()