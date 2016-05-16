"""Functions to prepair the data for injection injection
    elasticsearch"""
import json
import sys
from os import listdir
from os.path import join
import datetime
import index_expansion


STOP_WORDS = set(["artifact", 
                  "device",
                  "instrumentality"])

def read_json_data(file_name):
  """ Loads json data from file. """
  with open(file_name) as json_file:
    data = json.load(json_file)
  return data

def extract_descriptor(json_data):
  """Compile the thingscoop output into a long text string"""
  samples = [sample[1] for sample in json_data]
  words = [word[0].replace("_", " ") for sample in samples for word in sample[:1] ]
  return " ".join(words)

def read_video_data(path_to_video_data, nr_hypernyms):
  """Reads and prepairs the video data."""
  print "read video"
  file_names = listdir(path_to_video_data)
  data = {}
  exp_data = {}
  for name in file_names:
    if ".json" in name:
      json_data = read_json_data(join(path_to_video_data, name))
      data[name.split("_")[0]] = extract_descriptor(json_data)
      exp_data[name.split("_")[0]] = index_expansion.expand_index(data[name.split("_")[0]], nr_hypernyms)
  return data, exp_data

def duration_to_seconds(duration):
  """returns the total seconds in a "string formatted" duration hh:mm:ss"""
  h, m, s = map(int, duration.split(':'))
  return datetime.timedelta(hours=h, minutes=m, seconds=s).total_seconds()

def combine_json_data(meta_data_file_name, path_to_video_data, out_file_name, nr_hypernyms):
  """Combines the meta data with video descriptors and writes to a file."""
  print "combine"
  meta_data = read_json_data(meta_data_file_name)
  video_descriptors, expanded_descriptors = read_video_data(path_to_video_data, nr_hypernyms)
  data = []
  for (key, values) in meta_data.items():
    try:
      values["descriptor"] = video_descriptors[key]
      values["expanded_descriptor"] = expanded_descriptors[key]
      values["duration"] = duration_to_seconds(values["duration"])
    except KeyError:
      print "Video descriptor for {} was not found".format(key)
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
  print len(ARGV)
  if len(ARGV) == 1:
    print """usage: python combine_json_data.py <meta_data_file>
               <path_to_video_data> <out_file_name> <nr_hypernyms>\n"""
  elif ARGV[1] == "test":
    pass
  elif len(ARGV) == 5:
    META_DATA_FILE_NAME = ARGV[1]
    PATH_TO_VIDEO_DATA = ARGV[2]
    OUT_FILE_NAME = ARGV[3]
    NR_HYPERNYMS = int(ARGV[4])
    combine_json_data(META_DATA_FILE_NAME, PATH_TO_VIDEO_DATA, OUT_FILE_NAME, NR_HYPERNYMS)

