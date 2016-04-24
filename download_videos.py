from __future__ import unicode_literals
import youtube_dl

file = open("videourls.txt","r")
ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	""" Just an example video
	"""
	for url in file.readlines():
		print url
		ydl.download([url])
