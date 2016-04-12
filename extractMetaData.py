""" Module for extracting meta data for youtube videos given a
file of urls.  Requires pafy. """
import pafy
import json

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
    url_file_name = "urls.txt"
    meta_data_file_name = "meta.txt"
    extract_and_save_meta_data(url_file_name, meta_data_file_name)
    d = read_meta_data(meta_data_file_name)
    print json.dumps(d, sort_keys=True, indent=4, separators=(",", ":"))
