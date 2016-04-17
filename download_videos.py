from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	""" Just an example video
	"""
	ydl.download(['https://www.youtube.com/watch?v=wcGhCdEmeUM'])
