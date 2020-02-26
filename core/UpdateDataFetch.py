import pymysql
import time

# 设置流量输入查询的时间段
time2 = datetime.datetime.now()
time1 = time2 - datetime.timedelta(hours=1)
strtime1 = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
strtime2 = datetime.datetime.strftime(time2, '%Y-%m-%d %H:%M:%S')

print("查询时段{}~{}".format(strtime1, strtime2))
sql_vlm = "select * from volume_data where datetime between '{}' and '{}'".format(strtime1, strtime2)
sql_rtr = "select * from route_rate where datetime between '{}' and '{}'".format(strtime1, strtime2)
# 启动查询，错误报错退出
class Fetch:
    sql_vlm = "select * from volume_data where datetime between '{}' and '{}'".format(strtime1, strtime2)
    sql_rtr = "select * from route_rate where datetime between '{}' and '{}'".format(strtime1, strtime2)

    def __init__(self, time):
        self.conn = pymysql.connect(host="localhost", user="root", password='123456', database='traffic_test',
                               charset='utf8')
        self.cursor = conn.cursor()

        self.sql_vlm = "select * from volume_data where datetime between '{}' and '{}'".format(time, str((int(time[11:13])+1)))
        self.sql_rtr = "select * from route_rate where datetime between '{}' and '{}'".format(time, str((int(time[11:13])+1)))

    def fetchdata(self, sql):
        result = None
        try:
            # 执行SQL语句
            cursor_vlm.execute(sql)
            # 获取所有记录列表
            result = self.cursor.fetchall()
        except:
            print("Error: unable to fecth data")

        return result

    def volume(self):
        # 写进文件

        pass

    def route(self):
        # 写进文件
        pass
try:
    # 执行SQL语句
    cursor_vlm.execute(sql_vlm)
    # 获取所有记录列表
    results_vlm = cursor_vlm.fetchall()
    # return results
    # print(results_rtr[1])
except:
    print("Error: unable to fecth data")
    break

# 启动查询，错误报错退出
try:
    # 执行SQL语句
    cursor_rtr.execute(sql_rtr)
    # 获取所有记录列表
    results_rtr = cursor_rtr.fetchall()
    # return results
    # print(results_rtr[1])
except:
    print("Error: unable to fecth data")
    break

# 遍历并设置各流量输入点
volume_list = []
for i in range(len(results_vlm)):
    VI_number = results_vlm[i][1]
    new_volume = results_vlm[i][2]
    volume_list.append(new_volume)
    # print(new_volume)
    Vissim.Net.VehicleInputs.ItemByKey(VI_number).SetAttValue('Volume(1)', new_volume)
print('输入流量组为：', volume_list)

# 遍历并设置每个转向比
rate_list = []
for i in range(len(results_rtr)):
    instruction = results_rtr[i][1]
    decision = results_rtr[i][2]
    movement = results_rtr[i][3]
    rate = results_rtr[i][4]
    rate_list.append(rate)
    # print(instruction,decision,movement,rate)
    SVRD_number = results_rtr[i][2]  # SVRD = Static Vehicle Routing Decision
    SVR_number = results_rtr[i][3]  # SVR = Static Vehicle Route (of a specific Static Vehicle Routing Decision)
    new_relativ_flow = results_rtr[i][4]
    # print(new_relativ_flow)
    Vissim.Net.VehicleRoutingDecisionsStatic.ItemByKey(SVRD_number).VehRoutSta.ItemByKey(SVR_number).SetAttValue(
        'RelFlow(1)', new_relativ_flow)
print('转向比为：', rate_list)

conn.close()