import os
import time
from conf.config import *

def ReadTargetFile(path,hour):
    '''
    获取目标文件，返回生成器
    :param path: 历史流量文件夹
    :param hour: 当前小时数
    :return: 数据对应生成器
    '''
    filename = os.path.join(path, '{}.txt'.format(hour))
    with open(filename,encoding='utf-8') as f:
        while 1:
            l = f.readline()
            if l:
                yield l
            else:
                break

def WriteRealtimeFile(filename, content):
    '''
    将历史流量输入到缓存文件中
    :param filename: 缓存文件名称
    :param content: 输入内容
    :return: 无
    '''
    with open(filename,'w',encoding='utf-8') as f:
        for i in content:
            f.write(i)
    print('finish')

while 1:
    hour = time.localtime(time.time()).tm_hour
    if hour < 24:
        WriteRealtimeFile(volume_file,ReadTargetFile(VolumeHistory,hour))
        WriteRealtimeFile(routerate_file,ReadTargetFile(RateHistory,hour))
        print(hour)
        time.sleep(10)
    else:
        break