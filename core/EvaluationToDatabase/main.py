import pymysql

from conf.config import *




def main():
    # 实时获取三个文件内容
    # 如果有更新 则打开数据库 输入数据
    # 关闭数据库

def tail(filename):
    with open(filename, encoding='utf-8') as f:
        while 1:
            line = f.readline()
            if line.strip():
                yield line.strip()


g = tail(datacollection_file)
for i in g:
    print(i)