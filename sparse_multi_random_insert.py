# 优化问题
# 1.用户量有限。2.业务员有限。
# 现在假定业务员有一个步行速度为1.
# 考虑全局最优

# 接口1：初始化15个用户的各维度信息，并写入数据库
# 接口2：输入0个或多个业务员的坐标（最多10个，补齐到10个，随机生成）
import pymysql
import random
def user_info_interface():
    conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '123456',
    db = 'test',
    charset = 'utf8'
    )
    cursor = conn.cursor()
    list_of_locs = []
    for i in range(15):
        # a = input("请输入用户信息（编号，坐标x，坐标y）{0}，以空格分开：".format(i+1))
        # a = a.split(' ')
        list_of_locs.append([int(random.random()*1000000), float(random.random()*1000), float(random.random()*1000)])
    for loc in list_of_locs:
        sql = 'INSERT INTO user_info_test_1 VALUES({0}, {1}, {2});'.format(loc[0], round(loc[1], 2), round(loc[2], 2))
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()
user_info_interface()