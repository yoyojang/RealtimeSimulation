import pymysql

conn = pymysql.connect(host="localhost", user="root", password='123456', database='traffic_test', charset='utf8')
cursor_vlm = conn.cursor()
cursor_rtr = conn.cursor()

time2 = datetime.datetime.now()
time1 = time2 - datetime.timedelta(hours=1)
strtime1 = datetime.datetime.strftime(time1, '%Y-%m-%d %H:%M:%S')
strtime2 = datetime.datetime.strftime(time2, '%Y-%m-%d %H:%M:%S')

print("查询时段{}~{}".format(strtime1, strtime2))
sql_vlm = "select * from volume_data where datetime between '{}' and '{}'".format(strtime1, strtime2)
sql_rtr = "select * from route_rate where datetime between '{}' and '{}'".format(strtime1, strtime2)
# 启动查询，错误报错退出
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