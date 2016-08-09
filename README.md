# VK-Music-Downloader
Downloader of music from VK with command-line parameters and authorization config file.

1. pip install vk
2. edit the vk_music_downloader_auth.cfg by adding your auth information. 

usage: vk_music_downloader.py [-h] [-path PATH] [-artist ARTIST] [-title TITLE] [-show] [--sort]

By default it asks you — whether you really want DOWNLOAD ALL your tracks? ;-)

VK Music Downloader parameters.

optional arguments:
  -h, --help      show this help message and exit
  -path PATH      Path of download folder. Default: "Download"
  -artist ARTIST  Download the track(s) with specified Artist
  -title TITLE    Download the track(s) with specified Title
  -show           Show the track(s) without downloading
  --sort          Sort the track(s) by Artist. Default: by date of adding
