# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import os
import glob
from pathlib import Path
import parameters

### pull common variables from the parameters file
files_root = parameters.files_root

### make path
files_path = Path(files_root)

### create lists of images in each charts folder
files_list = files_path.glob('*')
schedules_list = files_path.glob('*schedule*')

for i in files_list:
    if i not in schedules_list:
        try:
            os.remove(i)
        except:
            print('Error while deleting file : ', i)

print('Flushed any preexisting (excluding schedule) files.')