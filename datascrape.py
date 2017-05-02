import os
import re
import sys
import glob
import errno
from sys import argv
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

script, presidentDir, writeDir = argv    
  
os.chdir(presidentDir)
i = 0
length = 0
for name in glob.glob("*.html"):
	i += 1
	print str(i)+': '+name
	try:
		with open(name) as f:
			html = f.read()
			parsed_html = BeautifulSoup(html)
			[s.extract() for s in parsed_html('script')]
			temp = open(writeDir+'/'+name.replace('.html',''),'w')
			s = parsed_html.body.getText(' ').encode('utf-8')
			length += len(s)
			temp.write(s)
			temp.close()
	except IOError as exc:
		if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
			raise

temp = open('properties','w')
temp.write('N '+str(i)+'\n')
temp.write('avg '+str(length/i))

