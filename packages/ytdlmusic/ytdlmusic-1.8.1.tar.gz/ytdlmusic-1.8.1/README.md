## Description

``ytdlmusic`` is a command-line program to search and download music files from YouTube without use browser. 

## Information

This package is directly available from [pypi](https://pypi.org/project/ytdlmusic/)

It may be illegal to download restricted content with this software, depending on the law in your country.

This package use two very important dependencies :
- [youtube_dl](https://pypi.org/project/youtube_dl/)
- [youtube-search-python](https://pypi.org/project/youtube-search-python/)

## Installation prerequisites

- Install Python 3 for your system
- Install pip3* for your system
- Install ffmpeg for your system if you want to use MP3/OGG format (M4A otherwise)

*_Install pip instead of pip3, if pip3 does not exist for your OS_
## Installation

``pip3 install ytdlmusic``*

*_Use pip instead of pip3, if pip3 does not exist_

## Use

``ytdlmusic [ARTIST] [SONG]``

ytdlmusic searches Youtube for "\[ARTIST\] \[SONG\]" and displays the top five result and their description. The selected result is  downloaded in your current directory. The format used is MP3 (default) or OGG. If ffmpeg is not installed, M4A is used. The filename is \[ARTIST\]\_\[SONG\].mp3/ogg to lowercase, with special characters replaced by '\_'. 

Example:
```
~$ ytdlmusic "Rexlambo" "Stay With Me"
search "Rexlambo Stay With Me" with youtube-search-python
1
Rexlambo - stay with me
https://www.youtube.com/watch?v=LrED6SSFf-I
3:52 - 9,196 views
2
stay with me – Rexlambo (No Copyright Music)
https://www.youtube.com/watch?v=a0hkrjqpIOo
3:52 - 165,489 views
3
Rexlambo - stay with me
https://www.youtube.com/watch?v=TjATW8iAwa0
3:52 - 658 views
4
Mon week-end de GT4 à Nogaro !
https://www.youtube.com/watch?v=erxK0DtIhYI
11:02 - 796 views
5
Rexlambo - stay with me
https://www.youtube.com/watch?v=0vnOMFmBUGk
3:52 - 831 views
Which (1-5, 0 to exit properly) ? 2
download https://www.youtube.com/watch?v=a0hkrjqpIOo with youtubedl
rexlambo_stay_with_me.mp3 is ready
````
## Batch

You can use a beta command to loop in a csv file, and download all MP3/M4A files from it. 

`` ytdlmusic --batch=path_file%had_header%sep%artist_column%song_column ``

Example :

```
ytdlmusic -y --batch="./test.csv"%True%";"%2%1
search "above limujii" with youtube-search-python
download https://www.youtube.com/watch?v=cUWU_T9KBk8 with youtubedl
above_limujii.mp3 is ready
search "awake nomyn" with youtube-search-python
download https://www.youtube.com/watch?v=hZQDfGX8Cu4 with youtubedl
awake_nomyn.mp3 is ready
search "zhhezhahkzaj eyazttyzaeyz" with youtube-search-python
No result, retry with other words
search "avalon scandinavianz" with youtube-search-python
download https://www.youtube.com/watch?v=B5CYUMs6-eo with youtubedl
avalon_scandinavianz.mp3 is ready
```

with csv file 
```
song_column;artist_column;unused column
limujii;above;no
nomyn;awake;use
eyazttyzaeyz;zhhezhahkzaj;inexistant
scandinavianz;avalon;information
```
## Other commands

`` ytdlmusic --check `` or `` ytdlmusic -c `` check if update is available for program

`` ytdlmusic --Check `` or `` ytdlmusic -c `` check if update are available for program and dependencies

`` ytdlmusic --update `` or `` ytdlmusic -u `` upgrades ytdlmusic

`` ytdlmusic --full-update `` or `` ytdlmusic -U `` upgrades ytdlmusic, youtube-dl and youtube-search-python

`` ytdlmusic --help`` or `` ytdlmusic -h `` displays help message

`` ytdlmusic --version `` or `` ytdlmusic -v `` displays version of ytdlmusic and dependencies

`` ytdlmusic`` displays help message, version, and license


## Other flags

You can also add these flags to your commands (except help and version) :


`` --auto `` or `` -y `` : use auto mode : choose first item for classic use, auto-accept for other commands. 

`` --n=X `` : number of choices (default=5, min=1, max=10)

`` --k `` or `` --keep `` : kepp the YouTube video title for the filename

`` --Q `` or `` --quality `` : if mp3, set quality to 320kbs instead of 256kbs

`` --quiet `` or `` -q `` : give less output 

`` --verbose `` or `` -d `` : give more output

`` --m4a `` or `` -f `` : force use m4a format

`` --ogg `` or `` -o `` : use ogg instead of mp3 format
## Local install to develop

```
git clone https://github.com/thib1984/ytdlmusic.git
cd ytdlmusic 
#work!
pip3 install . #to build
ytdlmusic "Rexlambo" "Stay With Me"  #to retest
pip3 uninstall ytdlmusic #to properly uninstall the dev version
``` 
 
## FAQ

### When i try to update youtube-dl with ``youtube-dl -U``, i obtain an error message in my debian/ubuntu

If you obtain the following message : 

```
It looks like you installed youtube-dl with a package manager, pip, setup.py or a tarball. Please use that to update.
```

instead of 

```
youtube-dl: error: youtube-dl's self-update mechanism is disabled on Debian.
Please update youtube-dl using apt(8).
See https://packages.debian.org/sid/youtube-dl for the latest packaged version.
```

, no panic! You have just downloaded a newer version of youtube-dl which is not in apt. When a new version of youtube-dl will be released in apt, you will download it automatically with ``sudo apt upgrade``. If you want to retrieve the previous version, ``sudo apt remove youtube-dl && sudo apt install youtube-dl``

### I would like a MP3 format but I only get an M4A format, why?

The ``ffmpeg`` package is required for the MP3 conversion. Install it and retry to launch ytdlmusic

### The commands indicated in this README don't work for me! Why?

The  syntax of the commands can be change between versions, run ``ytdlmusic`` and read the help message. 

### I get an error about ``_requesthandler.py line 22`` when I try to use ytdlmusic

Sorry... You should update Python to 3.6 version or more. youtube-search-python doesn't seems to be compatible with Python 3.5 or less. Now, ytdlmusic package checks the Python version during the installation process.

### What are the compatibilities with Python, pip, youtube-dl and youtube-search-python?

When an new version is released, it is compatible with the last Python version ine the branches 3.6 to 3.10, on the release date. It's also compatible with the last versions of dependencies, on the release date.

### Have you tested your package?

Before a new version of ytdlmusic is published, it is checked in an [automatic job](https://github.com/thib1984/ytdlmusic/actions/workflows/publish.yml), with the last versions of pip, youtube-dl and youtube-search-python, and also in the last versions of Python in the four branches 3.6 to 3.10.*

Each night, [another automatic job](https://github.com/thib1984/ytdlmusic/actions/workflows/test_published_release.yml) checks the actual package with last versions of dependencies and Pythons 3.6 to 3.10. So if a regression appears, the author of ytdlmusic received  an automatic mail to warn it.*

*_These tests are executed with GitHub Actions on an Ubuntu 20.04 image. Tests are also runned on macOS and Windows images (only very last Python version)._
## Thanks

Thanks to contributors and dependencies authors :

- [albenquer](https://github.com/albenquer) and [dlicois](https://github.com/dlicois) for contributions!
- [Hitesh Kumar Saini](https://github.com/alexmercerind) for [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
- [ytdl-org](https://github.com/ytdl-org) for [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [Federico Carboni](https://github.com/FedericoCarboni) for [setup-ffmpeg](https://github.com/FedericoCarboni/setup-ffmpeg)
- [pypa](https://github.com/pypa) for [gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
- [elgohrf](https://github.com/elgohr) for [Github-Release-Action](https://github.com/elgohr/Github-Release-Action)
## License

MIT License

Copyright (c) 2021 [thib1984](https://github.com/thib1984)


