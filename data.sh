#!/bin/bash
# Copy the image files to the archive directory.
#
export ANACONDA=3
. $HOME/.bashrc
set -x
python get_dc_data.py
