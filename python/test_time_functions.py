from datetime import datetime
import time
import json
from tweet import Tweet
from tracker import Tracker

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
datetime = "2021-02-26T14:36:38.000Z"
def reformat_date(date): 
    date = date.replace('-', ',')
    date = date.replace('T', ',')
    date = date.replace(':', ',')
    date = date.replace('.', ',')
    date = date.replace('Z', '')
    return date.split(',')

print(reformat_date(datetime))
date = datetime()