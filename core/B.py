import time
from multiprocessing import Pool
def bbb():
    while 1:
        print('b')
        time.sleep(3)
    if __name__ == '__main__':
        p = Pool()
