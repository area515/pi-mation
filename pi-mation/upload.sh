#!/bin/bash

echo "Looking for files to upload"
#loop over all files in upload directory
for f in ./upload/*; do
  filedate=$(echo $f |grep -Eo '[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}')
  filetime=$(echo $f |grep -Eo '[[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2}')
  echo $filedate
  echo $filetime
  echo "Working on $f file..."
  description="Raspberry Pi stop motion animation - Science Center of Iowa - created $filedate at $filetime"
  youtube-upload --email=stop.motion.pi.iowa@gmail.com --password="" --title="Stop motion video - $filedate $filetime" --description="$description" --category=Music --keywords="raspberrypi, stop-motion, sciowa" $f
  echo "Completed upload"
  echo "Removing file"
  rm $f
  echo "File removed"
done

echo "All files have been uploaded"


