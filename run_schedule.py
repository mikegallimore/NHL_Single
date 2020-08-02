# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import argparse

parser = argparse.ArgumentParser()

### creates arguments to make use of in functions
parser.add_argument('season_id', help='Set to [8-digit season number] (e.g. 20182019)')

args = parser.parse_args()

import schedule_fetch
schedule_fetch.parse_ids(args.season_id)
schedule_fetch