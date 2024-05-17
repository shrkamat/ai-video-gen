#!/bin/bash
# set up python 3.8 (google colab)
!sudo apt-get update -y
!sudo apt-get install python3.8 python3.8-distutils
from IPython.display import clear_output 
clear_output()
!sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Choose one of the given alternatives:
!sudo update-alternatives --config python3

# This one used to work but now NOT(for me)!
# !sudo update-alternatives --config python

# Check the result
!python3 --version

# Attention: Install pip (... needed!)
!sudo apt install python3-pip
