GAFpy is parser for gaf files
Written in Python by Oleksandr Kuznietsov <o.kuznietsov@gmail.com>
Supports Python v2.7 and v3

GAF converter can be downloaded from http://gafmedia.com

Usage:
```python
import GAFParser, os

gafFiles = [a for a in os.listdir('.') if os.path.isfile(a) and os.path.splitext(a)[1] == '.gaf']
for f in gafFiles:
	g = GAFParser.load(f)
	majorVersion = g['header']['majorVersion']
	minorVersion = g['header']['minorVersion']
	compressed = g['header']['compressed']
	print("GAF `{3}`\t v{0}.{1} \tCompressed {2}".format(majorVersion, minorVersion, compressed, f))
```
