import win32com.client as com


from conf.config import *
from core import MyCOM

class Evaluation:
    def __init__(self, obj, n, datetime):
        self.n = n
        self.obj = obj
        self.datetime = datetime

        
        att1 = {
            'No':'No',
            'TravTm': "TravTm(1,{},All)".format(n),
            'Vehs': "Vehs(1,{},All)".format(n),
            'DistTrav': "DistTrav(1,{},All)".format(n),
        }
        self.att_traveltime = [i for i in att1.values()]

        att2 ={
            'Node':'Node',
            'Edges':'Edges',
            'Qlen' : "QLen(1,{})".format(n),
            'QlenM' : "QLenMax(1,{})".format(n),
            'Vehs' : "Vehs(1,{},All)".format(n),
            'LOSVal' : "LOSVal(1,{},All)".format(n),
            'VehDelay' : "VehDelay(1,{},All)".format(n),
            'Stops' : "Stops(1,{},All)".format(n),
            'EmissionsCO' : "EmissionsCO(1,{})".format(n),
            'EmissionsNOx' : "EmissionsNOx(1,{})".format(n),
            'EmissionsVOC' : "EmissionsVOC(1,{})".format(n),
            'FuelConsumption' : "FuelConsumption(1,{})".format(n),
        }
        self.att_movement = [i for i in att2.values()]

        att3 = {
            'No':'No',
            'Acceleration': "Acceleration(1,{},All)".format(n),
            'Dist': "Dist(1,{},All)".format(n),
            'Length': "Length(1,{},All)".format(n),
            'Vehs': "Vehs(1,{},All)".format(n),
            'QueueDelay': "QueueDelay(1,{},All)".format(n),
            'SpeedAvgArith': "SpeedAvgArith(1,{},All)".format(n),
            'SpeedAvgHarm': "SpeedAvgHarm(1,{},All)".format(n),
            'OccupRate': "OccupRate(1,{},All)".format(n),
        }
        self.att_datacollection = [i for i in att3.values()]

    flag = StoreDBFlag


    def StoreLocal(self, file, lst):
        with open(file, 'a', encoding='utf-8') as f:
            date = self.datetime + ','
            f.write(date)
            for i in lst:
                cont = str(i) + ','
                f.write(cont)
            f.write('\n')

    def GettTravelTime(self):
        lst =  MyCOM.GetEvalTravelTime(self.obj, self.att_traveltime)
        Evaluation.StoreLocal(self, traveltime_file, lst)


    def GetMovement(self):
        lst =  MyCOM.GetEvalMovement(self.obj, self.att_movement)
        Evaluation.StoreLocal(self, movement_file, lst)


    def GetDatacollection(self):
        lst = MyCOM.GetEvalDataCollection(self.obj, self.att_datacollection)
        Evaluation.StoreLocal(self, datacollection_file, lst)


class MyVissim:
    def __init__(self, version, filename, flag_read_additionally=False):
        '''创建vissim对象并运行打开文件'''
        self.vissim = com.Dispatch(version)
        
        # self.vissim = self.vissim.Documents.Open(FileName = filename)
        self.vissim.LoadNet(filename, flag_read_additionally) #vissim软件用

    def signal_handle(self,SC_number, new_signal_program_number):
        '''信号方案更新'''
        MyCOM.SetProgNo(self.vissim, SC_number, new_signal_program_number)

    def volume_update(self, volume_file):
        '''流量更新'''
        with open(volume_file, encoding='utf8') as f:
            for i in f:
                point, volume = i.replace(' ', '').strip().split(',')
                # print(point,volume)
                MyCOM.SetVolume(self.vissim, point,volume)

    def route_update(self,routerate_file):
        '''路径转向比例匹配'''
        with open(routerate_file, encoding='utf8') as f:
            for i in f:
                p,q,rate = i.replace(' ', '').strip().split(',')
                # print(p, q, rate)
                MyCOM.SetRoute(self.vissim,p,q,rate)

    def GetAllCar(self):
        '''获取运行中的所有车辆信息'''
        info = ('VehType', 'Speed', 'Lane', 'Pos')
        lst = MyCOM.GetMultiCar(self.vissim, info)
        return lst

    def InAllCar(self,all_car_info):
        '''运行后立刻输入车辆'''
        for state in all_car_info:
            # ('100', 31.367223589909905, '26-1', 37.4414135474223)
            vehicle_type = int(state[0])
            desired_speed = state[1]  # unit according to the user setting in Vissim [km/h or mph]
            link, lane = [int(i) for i in state[2].split('-')]
            xcoordinate = state[3]
            MyCOM.SetNewCar(self.vissim, vehicle_type, link, lane, xcoordinate, desired_speed)

    def SetRunStartParam(self,firstbreaktime, endtime):
        '''设置仿真开始运行参数，第一次断点时间，总时长'''
        MyCOM.SetBreakTime(self.vissim, firstbreaktime)
        MyCOM.SetEndTime(self.vissim, endtime)

    def RunContinuous(self, breaktime,speed):
        '''继续运行，并设置下一断点及速度'''
        MyCOM.SetBreakTime(self.vissim, breaktime)
        MyCOM.SetRunSpeed(self.vissim,speed)
        MyCOM.RunContinuous(self.vissim)
    
    def GetEvaluation(self, n, datetime):
        # 评价模块
       return Evaluation(self.vissim,n, datetime)