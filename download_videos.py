from __future__ import unicode_literals
import youtube_dl
from os import path
import sys


ydl_opts = {}
if __name__ == "__main__":
	"""Usage python download_videos.py <url_file> <out_directory>"""
	file = open(sys.argv[1],"r")
	directory = sys.argv[2]
	ydl_opts = {'output':'id'}
	ydl_opts = {"outtmpl" : path.join(directory,r"%(id)s")}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		""" Just an example video
		"""
		for url in file.readlines():
			print url
			ydl.download([url])
