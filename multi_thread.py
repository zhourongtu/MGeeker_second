import single_thread
import threading
import random

class thread_process_yewu(threading.Thread):
    def __init__(self, func, args=()):
        super(thread_process_yewu, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)
    
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

# 按整数处理
def multi_yewu(list_of_locs):
    multi_to_process = []
    if(len(list_of_locs) < 100):
        for i in range(100 - len(list_of_locs)):
            list_of_locs.append([random.random() * 1000, random.random() * 1000])

    for my_loc in list_of_locs:
        x_loc_yewu = round(float(my_loc[0]), 2)
        y_loc_yewu = round(float(my_loc[1]), 2)
        t = thread_process_yewu(single_thread.query_nearest, args=(x_loc_yewu, y_loc_yewu))
        multi_to_process.append(t)
        t.start()
    
    ans = []
    for t in multi_to_process:
        t.join()
        ans.append([t.get_result()[0], t.get_result()[1], t.get_result()[2], t.getName()])
    
    for user, my_loc in zip(ans, list_of_locs):
        x_loc_yewu = round(float(my_loc[0]), 2)
        y_loc_yewu = round(float(my_loc[1]), 2)
        print('业务员坐标：', x_loc_yewu, y_loc_yewu)
        print('用户编号：', user[0], '用户坐标：', user[1], user[2], '处理线程名：', user[3])

list_of_locs = [[1.512, 2.213], [32,56], [102.54, 888.66], [825.5435, 666.66],[1.512, 2.213], [32,56], [102.54, 888.66], [825.5435, 666.66]]

multi_yewu(list_of_locs)

