#!/usr/bin/env python

import urllib
import re
import facedetect

def getRss():
	f = urllib.urlopen("http://f.hatena.ne.jp/twitter/rss")
	data = f.read()
	reg = re.compile("<hatena:imageurl>([\w\W]*?)</hatena:imageurl>")
	a = reg.findall(data)
	result = []
	for aa in a:
		result.append(aa)
	return result

if __name__ == "__main__":
	result = getRss()
	facedetect.miniFaceDetect(result)
