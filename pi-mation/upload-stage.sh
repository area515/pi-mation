#!/bin/bash

# expected: filename upload_dir
if [ ! $2 ]
then
  echo "usage: upload-stage.sh filename upload_dir"
  exit
fi

echo Moving $1 to $2/$(basename $1)_$(date +%F-%T)
mv $1 $2/$(basename $1)_$(date +%F-%T)
echo $1 staged to upload
