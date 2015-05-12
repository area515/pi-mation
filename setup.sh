#!/bin/bash

# gdata-python setup
# go home
cd ~
# git gdata-python
git clone https://github.com/google/gdata-python-client
# install gdata-python
sudo python setup.py install

#youtube-uploader setup
# go home
cd ~
# get youtube-uploader
wget http://youtube-upload.googlecode.com/files/youtube-upload-0.7.3.tgz
# untar
tar xvzf youtube-upload-0.7.3.tgz
# go into
cd youtube-upload-0.7.3/
# install youtube-uploader
sudo python setup.py install

# area515 pi-mation setup
# go home
cd ~
# git area515/pi-mation - you already did this to get here
#git clone https://github.com/area515/pi-mation
# go into
cd pi-mation/pi-mation
# chmod
chmod +x pi-mation.sh upload.sh upload-stage.sh
# add upload.sh to cron - run every 10 minutes
(crontab -l ; echo "*/10 * * * * ~/pi-mation/pi-mation/upload.sh") | crontab

