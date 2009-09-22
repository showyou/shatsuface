#!/usr/bin/env python

import urllib
import re
import facedetect

def getRss():
	f = urllib.urlopen("http://f.hatena.ne.jp/twitter/rss")
	data = f.read()
	reg = re.compile("<link>([\w\W]*?)</link>[\w\W]*?<hatena:imageurl>([\w\W]*?)</hatena:imageurl>")
	a = reg.findall(data)
	result = []
	for aa in a:
		print aa
		result.append((aa[0],aa[1]))
	return result
"""
	>>> putOut((1))
    1
"""
def putOut(result):
	for r in result:
		print "<a href=\"%s\"><img src=\"%s\"></a>" % r
	return

if __name__ == "__main__":
	fileNames = getRss()
	print "fileNames",fileNames
	result = facedetect.miniFaceDetect(fileNames)
	putOut(result)
