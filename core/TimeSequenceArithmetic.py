import time

from conf.config import *

'''
00:00:00, 06:00:00, 09:00:00, 11:00:00, 13:30:00, 16:00:00, 19:00:00, 21:00:00
3, 1, 1, 1, 2, 2, 3, 3
3, 1, 1, 2, 3, 4, 4, 5
3, 1, 2, 2, 3, 3, 4, 4
3, 1, 1, 2, 3, 4, 4, 5
'''
class TimeSeqArith:

    def __init__(self, file, now_time):
        self.file = file
        self.now_time = now_time

    def strtosecond(self,strtime):
        """将时间转化为秒"""
        li = [int(i) for i in strtime.strip().split(':')]
        return li[0] * 60 * 60 + li[1] * 60 + li[2]

    def gettimelist(self,time_list):
        '''将时间格式序列转化为秒序列'''
        label_time_list = []
        for i in time_list:
            label_time = self.strtosecond(i)
            label_time_list.append(label_time)
        label_time_list.append(86400 - 1)
        return label_time_list

    def getindex(self,nowtime,timelist):
        '''根据当前时间判断所在时间序列的不大于它的最大时间位置,并获得与后点的差'''
        # global i
        for i in range(len(timelist)):
            if nowtime < timelist[i]:
                break

        return i - 1, timelist[i] - nowtime

    def newseq(self,x,lst):
        '''根据时间位置，重新按顺序排列，位置处为第一个'''
        newlst = []
        li = [i for i in range(len(lst))]
        if x <= len(lst):
            # newli = li[x:] + li[:x] #24小时循环使用
            newli = li[x:]          #只到0点
            for i in newli:
                newlst.append(lst[i])
        return newlst

    def getinterval(self,lst):
        # 获取一个序列里的间隔差
        itv = []
        for i in range(len(lst)):
            if i < (len(lst)-1):
                interval = lst[i+1] - lst[i]
                itv.append(interval)
        return itv

    def main(self):
        '''主运行，返回运行时间序列，信号控制方案顺序'''
        intersection_signal_ProNo_list = []
        with open(self.file, encoding='utf-8') as f:
            time_list = f.readline().strip().split(',')
            label_time_list = self.gettimelist(time_list)    #处理第一行时间列表
            idx, first_run_time = self.getindex(self.now_time, label_time_list)     #确定当前时间所在区间
            # print(i, type(i))
            time_interval_list = self.getinterval(label_time_list)
            new_time_interval_list = self.newseq(idx, time_interval_list) # 仿真中时间序列，更新信号控制
            new_time_interval_list[0] = first_run_time
            # 更新所有交叉口的序列顺序
            for i in f:
                oldlst = [int(j) for j in i.strip().split(',')]
                newlst = self.newseq(idx, oldlst)
                intersection_signal_ProNo_list.append(newlst)
        return  new_time_interval_list, intersection_signal_ProNo_list