import pymysql

from conf.config import *


def tail(filename):
    with open(filename, encoding='utf-8') as f:
        while 1:
            line = f.readline()
            if line.strip():
                yield line.strip()


g = tail(datacollection_file)
for i in g:
    print(i)
