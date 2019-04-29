# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 21:10:47 2017

@author: @mikegallimore
"""

import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set the season (e.g. 20182019)')

args = parser.parse_args()

import schedule_fetch
schedule_fetch.parse_ids(args.season_id)
schedule_fetch