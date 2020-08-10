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
        a = input("请输入用户信息（编号，坐标x，坐标y）{0}，以空格分开：".format(i+1))
        a = a.split(' ')
        list_of_locs.append([int(a[0]), float(a[1]), float(a[2])])
    for loc in list_of_locs:
        sql = 'INSERT INTO user_info_test_1 VALUES({0}, {1}, {2});'.format(loc[0], round(loc[1], 2), round(loc[2], 2))
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()


def yewuyuan_info_interface(locs_of_yewuyuan):
    if(len(locs_of_yewuyuan) < 10):
        for i in range(10 - len(locs_of_yewuyuan)):
            locs_of_yewuyuan.append([round(random.random() * 1000, 2), round(random.random() * 1000, 2)])
    # 到这里，需要处理业务员需要的一个距离
        
    # 实践1：最近分类原则
    conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '123456',
    db = 'test',
    charset = 'utf8'
    )
    cursor = conn.cursor()
    sql = 'select * from user_info_test_1;'
    cursor.execute(sql)
    datas = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    distance_dict = {}
    for i in range(len(locs_of_yewuyuan)):
        distance_dict[i+1] = []
    for data in datas:
        all_distance = []
        for yewuyuan in locs_of_yewuyuan:
            temp_distance = (float(data[1]) - yewuyuan[0]) ** 2 + (float(data[2]) - yewuyuan[1]) ** 2
            all_distance.append(temp_distance)
        nearest_index = all_distance.index(min(all_distance))
        distance_dict[nearest_index+1].append(data)
    
    for yewuyuan, loc in zip(range(len(locs_of_yewuyuan)), locs_of_yewuyuan):
        print('业务员编号：', yewuyuan+1, '业务员坐标：', loc[0], loc[1])
        i = 1
        for user in distance_dict[yewuyuan+1]:
            print('用户{0}编号：'.format(i+1), user[0], '用户坐标：', user[1], user[2])
            i = i+1