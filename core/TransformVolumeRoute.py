import os
from conf.config import *

volume_path = VolumeHistory
rate_path = RateHistory
n = 0
while n < 24:
    n += 1
    filename = os.path.join(VolumeHistory, '{}.txt'.format(i))
    with open(filename, encoding='utf-8') as f:
        
