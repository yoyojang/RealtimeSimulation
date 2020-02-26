import time
# import win32com.client as com

from conf.config import *
from core.MyVissim import MyVissim
from core.TimeSequenceArithmetic import TimeSeqArith
from core.DynamicSpeedArithmetic import DynamicSpeedArithmetic


# vissim = MyCOM(vissim_version)
def strtosecond(strtime):
    """将时间转化为秒"""
    li = [int(i) for i in strtime.strip().split(':')]
    return li[0] * 60 * 60 + li[1] * 60 + li[2]


def main():
    # 加载模型
    # 设置间隔时间，仿真总时长
    # 获取信号控制方案划分时段序列（时间控制序列算法）
    # 交通信号控制匹配，vissimcom
    myvissim = MyVissim(vissim_version, vissim_file_path)
    interval_time = update_interval_time
    output = output_multiple
    start_time = strtosecond(time.strftime("%X"))
    run_time_list, all_signal_list = TimeSeqArith(signal_program, start_time).main()
    # print(start_time, run_time_list, all_signal_list)

    speed = 0
    all_car = None

    for i in range(len(run_time_list)):
        # 信号控制匹配
        endtime = run_time_list[i]
        print('总时长：', endtime)
        mulriple = endtime // interval_time
        remainder = endtime % interval_time
        for k, v in intersection_info.items():
            signal_num = v[0]
            for each in all_signal_list:
                myvissim.signal_handle(signal_num, each[i])
        # 仿真开始运行参数设置
        if i == 0:
            myvissim.SetRunStartParam(interval_time, endtime)
        else:
            myvissim.SetRunStartParam(interval_time, endtime)
            myvissim.RunContinuous(1, speed)
            '''放置上次仿真的所有车辆'''
            myvissim.InAllCar(all_car)  # 输入方法再确认
        n = 0
        flag = True
        while flag:
            n += 1
            '''计算动态速度'''
            if n > 1:
                simutime = strtosecond(time.strftime("%X")) - start_time
                realtime = n * interval_time
                speed = DynamicSpeedArithmetic(realtime, simutime).main()
            fetch_time = time.strftime("%Y-%m-%d %X")
            myvissim.volume_update(volume_file)
            myvissim.route_update(routerate_file)

            if remainder > 0:
                if n <= mulriple:
                    breaktime = n * interval_time
                    print(breaktime)
                    myvissim.RunContinuous(breaktime, speed)
                else:
                    flag = False
                    breaktime = endtime - 1
                    print('***', breaktime)
                    myvissim.RunContinuous(breaktime, speed)
                    '''获取所有车辆，继续运行1s'''
                    lst = myvissim.GetAllCar()
                    all_car = lst
            else:
                if n < mulriple:
                    breaktime = n * interval_time
                    print(breaktime)
                    myvissim.RunContinuous(breaktime, speed)
                else:
                    flag = False
                    breaktime = endtime - 1
                    print('***', breaktime)
                    myvissim.RunContinuous(breaktime, speed)
                    '''获取所有车辆，继续运行1s'''
                    lst = myvissim.GetAllCar()
                    all_car = lst

                # 继续
                myvissim.vissim.Simulation.RunContinuous()
                print(all_car)

            if n % output == 0:
                datetime = time.strftime('%Y-%m-%d %X')
                evaluation = myvissim.GetEvaluation(n, datetime)
                evaluation.GetDatacollection()
                evaluation.GettTravelTime()
                evaluation.GetMovement()

