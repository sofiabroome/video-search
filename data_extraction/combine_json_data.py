"""Functions to prepair the data for injection injection
    elasticsearch"""
import json
import sys
from os import listdir
from os.path import join

def read_json_data(file_name):
  """ Loads json data from file. """
  with open(file_name) as json_file:
    data = json.load(json_file)
  return data

def extract_descriptor(json_data):
  """Compile the thingscoop output into a long text string"""
  samples = [sample[1] for sample in json_data]
  words = [word[0].replace("_", " ") for sample in samples for word in sample]
  return " ".join(words)

def read_video_data(path_to_video_data):
  """Reads and prepairs the video data."""
  print "read video"
  file_names = listdir(path_to_video_data)
  data = {}
  for name in file_names:
    if ".json" in name:
      json_data = read_json_data(join(path_to_video_data, name))
      data[name.split("_")[0]] = extract_descriptor(json_data)
  return data

def combine_json_data(meta_data_file_name, path_to_video_data, out_file_name):
  """Combines the meta data with video descriptors and writes to a file."""
  print "combine"
  meta_data = read_json_data(meta_data_file_name)
  video_descriptors = read_video_data(path_to_video_data)
  data = []
  for (key, values) in meta_data.items():
    try:
      values["descriptor"] = video_descriptors[key]
    except KeyError:
      print "video descriptor for {} was not found".format(key)
    data.append(values)

  with open(out_file_name, 'w') as out_file:
    elastic_index_cmd = "{ \"index\": {}}\n"
    for datum in data:
      datum = json.dumps(datum)
      out_file.write(elastic_index_cmd)
      out_file.write(datum+"\n")

  return data

if __name__ == "__main__":
  ARGV = sys.argv
  print ARGV
  if len(ARGV) == 1:
    print """usage: python combine_json_data.py <meta_data_file>
               <path_to_video_data> <out_file_name>\n"""
  elif ARGV[1] == "test":
    pass
  elif len(ARGV) == 4:
    META_DATA_FILE_NAME = ARGV[1]
    PATH_TO_VIDEO_DATA = ARGV[2]
    OUT_FILE_NAME = ARGV[3]
    combine_json_data(META_DATA_FILE_NAME, PATH_TO_VIDEO_DATA, OUT_FILE_NAME)

