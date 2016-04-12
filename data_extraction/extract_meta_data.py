""" Module for extracting meta data for youtube videos given a
file of urls.  Requires pafy and youtube-dl. """
import pafy
import json
import sys

def get_data(url):
  """ Extracts the meta data from the youtube site and stores
  relevant fields in a dictionary. """
  datum = {}
  video = pafy.new(url)
  datum['url'] = url.strip()
  datum['description'] = video.description
  datum['author'] = video.author
  datum['duration'] = video.duration
  datum['dislikes'] = video.dislikes
  datum['likes'] = video.likes
  datum['category'] = video.category
  datum['keywords'] = video.keywords
  datum['published'] = video.published
  datum['length'] = video.length
  datum['title'] = video.title
  datum['username'] = video.username
  datum['viewcount'] = video.viewcount
  datum['rating'] = video.rating

  return datum

def extract_and_save_meta_data(url_file_name, meta_data_file_name):
  """ Calls the metadataextractor for every url in the file name passed
  as an argument. """
  with open(url_file_name) as url_file:
    urls = url_file.readlines()
    meta_data = {url.strip():get_data(url.strip()) for url in urls}

  meta_data = json.dumps(meta_data)

  with open(meta_data_file_name, 'w') as out_file:
    out_file.write(meta_data)

def read_meta_data(file_name):
  """ Loads json data from file. """
  with open(file_name) as meta_file:
    meta = json.load(meta_file)
  return meta

if __name__ == "__main__":
  ARGV = sys.argv
  if len(ARGV) == 1:
    print """usage: python extractMetaData.py <url_file> <outfile>\n"""
  elif ARGV[1] == "test":
    URL_FILE_NAME = "urls.txt"
    META_DATA_FILE_NAME = "meta.txt"
    extract_and_save_meta_data(URL_FILE_NAME, META_DATA_FILE_NAME)
    TMP = read_meta_data(META_DATA_FILE_NAME)
    print json.dumps(TMP, sort_keys=True, indent=4, separators=(",", ":"))
  elif len(ARGV) == 3:
    URL_FILE_NAME = ARGV[1]
    META_DATA_FILE_NAME = ARGV[2]
    extract_and_save_meta_data(URL_FILE_NAME, META_DATA_FILE_NAME)
