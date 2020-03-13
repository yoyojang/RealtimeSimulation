#监听文件 实时输入数据库
# 与主程序同时运行，并在主程序结束后结束

import pymysql
import re
from multiprocessing import Process

from conf.config import *




def listen(filename):
    with open(filename, encoding='utf-8') as f:
        Flag = True
        while Flag:
            line = f.readline()
            if line.strip():
                if 'finish' in line:
                    Flag = False
                else:
                    yield line.strip()


def StrToNum(k):
    for j in range(len(k)):
        if 'None' in k[j]:
            k[j] = None
        elif '.' in k[j]:
            k[j] = float(k[j])
        else:
            # print(k[j])
            k[j] = int(k[j].replace("'", ''))
    return k

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
                k[j] = int(k[j].replace("'",''))
        k.insert(0, date)
        k = tuple(k)
        k_lst.append(k)
        return k_lst

def main(file,sql):
    listen_each = listen(file)
    for each in listen_each:
        if each:
            conn = pymysql.connect(host="172.192.10.101", user="root", password='123456', database='trsp', charset='utf8')
            cursor = conn.cursor()
            k_lst = handle_obj(each)
            try:
                cursor.executemany(sql, k_lst)
                conn.commit()
            except:
                print("无法插入流量")
            print('完成')
            conn.close()

def main_movement(file,sql_edge,sql_node):
    listen_each = listen(file)
    for each in listen_each:
        if each:
            conn = pymysql.connect(host="172.192.10.101", user="root", password='123456', database='trsp', charset='utf8')
            cursor = conn.cursor()
            date = each[:19]
            # 使用正则取出当前时间每个检测器数据
            obj_group = re.findall('(\([^\)]*\))', each)
            # print(obj_group)
            edge_lst = []
            node_lst = []
            for i in obj_group:
                # 把每个检测器数据分割，并将字符串转化为数字
                k = i[1:-1].strip().replace(' ', '').split(',')
                # print(k)
                if "''" in k[1]:
                    del k[1]
                    k = StrToNum(k)
                    k.insert(0, date)
                    node_lst.append(tuple(k))
                else:
                    del k[0]
                    k = StrToNum(k)
                    k.insert(0, date)
                    edge_lst.append(tuple(k))
                # print(node_lst,edge_lst)
            try:
                cursor.executemany(sql_edge, edge_lst)
                cursor.executemany(sql_node, node_lst)
                conn.commit()
            except:
                print("无法插入流量")
            print('完成')
            conn.close()


# if __name__ == '__main__':
#     sql_trvtm = "insert into traveltime() values(%s,%s,%s,%s,%s)"
#     sql_node = "insert into node_movement() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#     sql_edge = "insert into edge_movement() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#     sql_datacollection = "insert into datacollection() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#
#     p1 = Process(target=main, args=(datacollection_file,sql_datacollection,))
#     p2 = Process(target=main, args=(traveltime_file,sql_trvtm,))
#     p3 = Process(target=main_movement, args=(movement_file,sql_edge,sql_node,))
#     p1.start()
#     p2.start()
#     p3.start()
#     p1.join()
#     p2.join()
#     p3.join()
#     print('finish')
