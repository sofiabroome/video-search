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

def extract_and_save_meta_data(urlFileName, metaDataFileName):
    """ Calls the metadataextractor for every url in the file name passed
    as an argument. """
    with open(urlFileName) as url_file:
        urls = url_file.readlines()
        metaData = {url.strip():get_data(url.strip()) for url in urls}

    metaData = json.dumps(metaData, sort_keys=True, indent=4, separators=(",", ":"))

    with open(metaDataFileName,'w') as out_file:
        out_file.write(metaData)

def read_meta_data(fileName):
    """ Loads json data from file. """
    with open(fileName) as meta_file:
        meta = json.load(meta_file)
    
    return meta

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        print """usage: python extractMetaData.py <url_file> <outfile>\n
                """
    elif argv[1] == "test":
        url_file_name = "urls.txt"
        meta_data_file_name = "meta.txt"
        extract_and_save_meta_data(url_file_name, meta_data_file_name)
        d = read_meta_data(meta_data_file_name)
        print json.dumps(d, sort_keys=True, indent=4, separators=(",", ":"))
    
    elif len(argv) == 3:
        url_file_name = argv[1]
        meta_data_file_name = argv[2]
        extract_and_save_meta_data(url_file_name, meta_data_file_name)



