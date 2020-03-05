#监听文件 实时输入数据库
# 与主程序同时运行，并在主程序结束后结束

import pymysql
import re

from conf.config import *




def listen(filename):
    with open(filename, encoding='utf-8') as f:
        while 1:
            line = f.readline()
            if line.strip():
                yield line.strip()

def handle_obj(each):
    date = each[:19]
    # 使用正则取出当前时间每个检测器数据
    obj_group = re.findall('(\([^\)]*\))', each)
    # print(x)
    k_lst = []
    for i in obj_group:
        # 把每个检测器数据分割，并将字符串转化为数字
        k = i[1:-1].strip().split(',')
        # print(k)
        for j in range(len(k)):
            if 'None' in k[j]:
                k[j] = None
            elif '.' in k[j]:
                k[j] = float(k[j])
            else:
                # print(k[j])
                k[j] = int(k[j])
        k.insert(0, date)
        k = tuple(k)
        k_lst.append(k)
        return k_lst

def handle_movement(each):
    pass

def main(file,sql):
    listen_each = listen(file)
    for each in listen_each:
        k_lst = handle_obj(each)
        try:
            cursor.executemany(sql, k_lst)
            conn.commit()
        except:
            print("无法插入流量")

def main_movement(file,sql_edge,sql_node):
    pass

sql_trvtm = "insert into traveltime() values(%s,%s,%s,%s,%s)"
sql_node = "insert into node_movement() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_edge = "insert into edge_movement() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_datacollection = "insert into datacollection() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

# conn = pymysql.connect(host="localhost", user="root", password='123456', database='traffic_test',
#                                    charset='utf8')
# cursor = conn.cursor()
conn = pymysql.connect(host="172.192.10.101", user="root", password='123456', database='trsp',charset='utf8')
cursor = conn.cursor()

main(datacollection_file,sql_datacollection)
main(traveltime_file,sql_trvtm)
# main(movement_file)

conn.close()