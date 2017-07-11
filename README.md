![Supported Python versions](https://img.shields.io/badge/python-2.7-blue.svg) ![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)

# OSPRAI
Open Source Picture Review &amp; Analysis Investigator

A work in progress modular open source media categoriser and analysis tool, developed in Python 2.7, GTK 3, and Glade 3.18.

## Development Enviroment:

###### Windows
For those who wish to develop this project on Microsoft Windows, you will require the All-In-One PyGI/PyGObject Installer which can be obtained [here](https://sourceforge.net/projects/pygobjectwin32/files/)

The "dir_parser" module is dependant on:
OpenCV 2.x library - Available [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)
Example: pip install opencv_python‑2.4.13.2‑cp27‑cp27m‑win32.whl

NumPy
Example: pip install numpy

XXHash Library - Available [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#xxhash)

###### Ubuntu
You can install OpenCV from the Ubuntu or Debian repository via the command: sudo apt-get install libopencv-dev python-opencv

###### MacOS
To develop on MacOS you must first install the Homebrew package manager for MacOS which is obtained by running the following command: /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

You will then need to use homebrew and pip to install the following packages (tested using MacOS 10.12 - Sierra), the commands are listed as follows (the system may need to be restarted before running Osprai):

brew install gtk+3
brew install pygobject3
brew tap homebrew/science
brew install opencv
pip install numpy
brew install xxhash
pip install xxhash

## Sample Data:
It is accepted that developers may require large sample datasets for development. Refer to "sample_data.py" for a simple script that crawls NASA's Astronomy Picture of the Day archive and downloads the images. The author of this code is [Cecil Woebker](https://github.com/cwoebker)


