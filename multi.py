import multiprocessing as mul
import time
import os
import re
import threading
from utils.mylog import log_init


def f2():
    a = 1
    def f3():
        b = a * 2
        return b
    print(f3())



def f(x):
    time.sleep(1)
    return x ** 2

def f1(x):
    time.sleep(1)
    return       

def MultiProcess(num):

    with mul.Pool(num) as p:
        # res = p.map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        p.map(f1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

if __name__ == '__main__':
    # MultiProcess(1)
    # MultiProcess(2)
    # MultiProcess(5)
    # MultiProcess(None)
    # logger = log_init()
    # num = 1
    # logger.info(f"start! using {num if num else 'default'} core")
    # start_time = time.time()
    # # # t = threading.Thread(target=MultiProcess, args=(num,))
    # # # t.start()
    # # # while t.is_alive():
    # # #     pass
    # MultiProcess(num)
    # piece = time.time()-start_time
    # logger.info(f"end! took {piece:.3f}s")
    # f2()
    # key = [key[i+1:(i+1 + key[i + 1:].find(' ')) if key[i + 1:].find(' ') != -1 else len(key) - 1] for i in range(len(key)) if (key[i] == ' ' or key[i] == '[') and key[i+1].isnumeric()]
    # a, b, c = key
    # [print(i) for i in key if i.isnumeric()]
    # key = '[2    0   0]'
    # num_list = []
    # for i in range(len(key)):
    #     if (key[i] == ' ' or key[i] == '[') and key[i+1].isnumeric():
    #         end = (i+1 + key[i + 1:].find(' ')) if key[i + 1:].find(' ') != -1 else len(key) - 1
    #         num_list.append(key[i+1:end])
    # a, b, c = num_list
    # print(int(a), int(b), int(c))
    a = [[0,0,0],[0,1,0]]
    print(a.index([0,1,0]))