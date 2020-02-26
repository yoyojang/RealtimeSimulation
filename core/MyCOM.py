def SetProgNo(obj,SC_number, new_signal_program_number):
    '''
    修改对应信号机的信号控制方案
    :param SC_number: 信号机序号
    :param new_signal_program_number: 需新设置的信号方案序号
    :return: 无
    '''
    SignalController = obj.Net.SignalControllers.ItemByKey(SC_number)
    SignalController.SetAttValue('ProgNo', new_signal_program_number)

def clear_vissim_db(obj):
    '''
    清理vissim运行缓存的db文件
    :return:
    '''
    for simRun in obj.Net.SimulationRuns:
        obj.Net.SimulationRuns.RemoveSimulationRun(simRun)

# 仿真运行参数设置
def SetRunSpeed(obj,speed = 0):
    '''
    设置仿真运行速度，默认 0 ，运行最大速度；
    :param speed: float
    '''
    if speed:
        obj.Simulation.SetAttValue('UseMaxSimSpeed', False)
        obj.Simulation.SetAttValue('SimSpeed', speed)
    else:
        obj.Simulation.SetAttValue('UseMaxSimSpeed', True)

def SetRunBreak(obj,break_time):
    '''设置中断断时间'''
    obj.Simulation.SetAttValue('SimBreakAt', break_time)


def SetVolume(obj, VI_number, new_volume):
    '''
    设置流量
    :param obj:
    :param VI_number: 车辆输入点
    :param new_volume: 流量
    :return:
    '''
    obj.Net.VehicleInputs.ItemByKey(VI_number).SetAttValue('Volume(1)', new_volume)

def SetRoute(obj, SVRD_number, SVR_number, new_relative_flow):
    '''
    设置静态路径转向比例
    :param obj: vissim对象
    :param SVRD_number: 路径决策点
    :param SVR_number:决策点方向代号
    :param new_relative_flow: 相对比例值
    :return:
    '''
    obj.Net.VehicleRoutingDecisionsStatic.ItemByKey(SVRD_number).VehRoutSta.ItemByKey(SVR_number).SetAttValue(
        'RelFlow(1)', new_relative_flow)

def SetNewCar(obj, vehicle_type, link, lane, xcoordinate, desired_speed, interaction = False):
    '''
    放置新车辆
    :param obj:
    :param vehicle_type: 车辆类型
    :param link: 所在link
    :param lane: 所在车道
    :param xcoordinate: 位置，米
    :param desired_speed: 期望速度
    :param interaction: 是否互相影响，默认是
    :return:
    '''
    obj.Net.Vehicles.AddVehicleAtLinkPosition(vehicle_type, link, lane, xcoordinate, desired_speed, interaction)

def RunContinuous(obj):
    obj.Simulation.RunContinuous()

def SetBreakTime(obj,breaktime):
    obj.Simulation.SetAttValue('SimBreakAt', breaktime)

def SetEndTime(obj, endtime):
    obj.Simulation.SetAttValue('SimPeriod', endtime)

def GetMultiCar(obj, info):
    car_tpl = obj.Net.Vehicles.GetMultipleAttributes(info)
    return car_tpl

def GetEvalTravelTime(obj,att):
    # 车辆行程时间
    Veh_TT_measurement = obj.Net.VehicleTravelTimeMeasurements
    TravelTimeValue = Veh_TT_measurement.GetMultipleAttributes(att)
    return TravelTimeValue

def GetEvalMovement(obj, att):
    # MOVEMENT
    NodeGroup = obj.Net.Nodes
    NodeEdgeTotalList = []
    for each in NodeGroup:
        NodeEdgeTotal = each.Movements.GetMultipleAttributes(att)
        NodeEdgeTotalList += NodeEdgeTotal
    return NodeEdgeTotalList

def GetEvalDataCollection(obj, att):
    # 路段数据采集datacollection
    Datacollection = obj.Net.DataCollectionMeasurements
    DatacollectionValue = Datacollection.GetMultipleAttributes(att)
    return DatacollectionValue
