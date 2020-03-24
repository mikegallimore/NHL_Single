# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import parameters
from pathlib import Path

### pull common variables from the parameters file
files_root = parameters.files_root
files_20062007 = parameters.files_20062007

pbp_20062007 = Path(files_20062007).glob('*_pbp.csv')

header_saved = False
with open(files_root + '20062007_pbp_master.csv', 'w', newline='') as fileout:
    for filename in pbp_20062007:
        with open(str(filename)) as filein:
            header = next(filein)
            if not header_saved:
                fileout.write(header)
                header_saved = True
            for line in filein:
                fileout.write(line)
                
                
print('Finished binding the 20062007 play-by-play copies.')