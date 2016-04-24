#!/bin/bash
mkdir videos
python data_extraction/extract_meta_data.py data_extraction/urls.txt data_extraction/meta.txt
python download_videos.py data_extraction/urls.txt videos

for i in $( ls videos ); do
	file="videos/$i"
	echo $file
	descriptor="$file_googlenet_places.json"
	# if [ ! -f $descriptor ]; then
	thingscoop describe $file -m googlenet_places
	# fi
done

python data_extraction/combine_json_data.py data_extraction/meta.txt videos data.json