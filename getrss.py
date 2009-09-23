#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import re
import facedetect

#htmlPath = "."
htmlPath = "/home/yuki/public_html"
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
def putOutRSS(result):
	f = open(htmlPath+"/rss.rdf","w")
	f.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
	f.write("<rdf:RDF\n" \
	    "xmlns=\"http://purl.org/rss/1.0/\" \n" \
	    "xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" \n" \
	    "xmlns:content=\"http://purl.org/rss/1.0/modules/content/\" \n" \
	    "xmlns:dc=\"http://purl.org/dc/elements/1.1/\" \n" \
		"xml:lang=\"ja\">\n")
	f.write("<channel rdf:about=\"http://showyou.ath.cx/shatsuface/rss.rdf\">\n")
	f.write(" <title>顔写ツ</title>\n")
	f.write(" <link>http://showyou.ath.cx/</link>\n")
	f.write(" <description>写ツから人の顔と判定されたものを表示してます</description>\n")
	f.write("</channel>\n")
	for r in result:
		f.write("<item rdf:about=\"%s\">\n" % r[0])
		f.write(" <title>%s</title>\n" % r[1])
		f.write(" <link>%s</link>\n" % r[0])
		f.write(" <description><![CDATA[<a href=\"%s\"><img src=\"%s\" /></a>]]></description>\n" % r)
		f.write("</item>\n")
	f.write("</rdf:RDF>\n")	
	return

def putOut(result):
	f = open(htmlPath+"/index.html","a")
	for r in result:
		f.write ("<a href=\"%s\"><img src=\"%s\"></a>" % r)

if __name__ == "__main__":
	fileNames = getRss()
	print "fileNames",fileNames
	result = facedetect.miniFaceDetect(fileNames)
	putOut(result)
	putOutRSS(result)
