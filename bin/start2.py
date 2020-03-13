from multiprocessing import Process

from os import getcwd, path
from sys import path as sys_path
sys_path.insert(0, path.dirname(getcwd()))

from core.EvaluationToDatabase import main
from conf.config import *

if __name__ == '__main__':
    if __name__ == '__main__':
        sql_trvtm = "insert into traveltime() values(%s,%s,%s,%s,%s)"
        sql_node = "insert into node_movement() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_edge = "insert into edge_movement() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_datacollection = "insert into datacollection() values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        p1 = Process(target=main.main, args=(datacollection_file, sql_datacollection,))
        p2 = Process(target=main.main, args=(traveltime_file, sql_trvtm,))
        p3 = Process(target=main.main_movement, args=(movement_file, sql_edge, sql_node,))
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
        print('finish')