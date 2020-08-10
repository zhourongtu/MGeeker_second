import math
import pymysql

# 查询数据库，获取相应的方法
def query_nearest(x_loc_yewu, y_loc_yewu):
    # 连接数据库
    conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '123456',
    db = 'test',
    charset = 'utf8'
    )
    cursor = conn.cursor()

    # 业务逻辑：获取最近的一个用户
    x_loc = round(x_loc_yewu, 2)
    y_loc = round(y_loc_yewu, 2)
    x_block = int(x_loc)
    y_block = int(y_loc)
    x_limit_l = x_block
    x_limit_r = x_block
    y_limit_l = y_block
    y_limit_r = y_block
    flag = False # 用于指示是否找到最近的那个值
    # 考虑到可能存在的问题，需要进行expand 圆形处理。（当前查找的范围放大根号2倍，再处理一次。包含可能遗漏的区域。
    # while(False == flag):
    while(not(x_limit_l == 0 and x_limit_r == 1000 and y_limit_l == 0 and y_limit_r == 1000)):
        x_limit_l, x_limit_r, y_limit_l, y_limit_r = expand_range_plus_one([x_limit_l, x_limit_r, y_limit_l, y_limit_r])
        # 查找通过动态变化x_limit_l, x_limit_r, y_limit_l, y_limit_r，单独写一个函数，进行扩展
        sql = 'select id, x_loc, y_loc from user_info where x_block >= {0} and x_block <= {1} and y_block >= {2} and y_block <= {3}'.format(x_limit_l, x_limit_r, y_limit_l, y_limit_r)
        cursor.execute(sql)
        datas = cursor.fetchall()
        # TODO 查找距离最近的同学
        if(datas != ()):
            flag = True
            break
        else:
            pass
            continue #下一个范围继续查找

    # 解决问题2，进行根号二倍放大
    if(flag): 
        x_limit_l, x_limit_r, y_limit_l, y_limit_r = expand_range_times_sqrt2([x_limit_l, x_limit_r, y_limit_l, y_limit_r])
        sql = 'select id, x_loc, y_loc from user_info where x_block >= {0} and x_block <= {1} and y_block >= {2} and y_block <= {3}'.format(x_limit_l, x_limit_r, y_limit_l, y_limit_r)
        cursor.execute(sql) # 这里不存在rollback的情况，不写try catch了
        datas = cursor.fetchall()
        my_dict = {}
        for data in datas: # 进行处理与排序，如果距离相同，比较用户id大小，做替换
            distance = round((float(data[1])-x_loc_yewu)**2 + (float(data[2])-y_loc_yewu)**2, 4)
            if(distance in my_dict):
                if(my_dict[distance][0] > data[0]): #用户编号更小
                    my_dict[distance] = data
            else:
                my_dict[distance] = data
        result = sorted(my_dict.items(),key=lambda my_dict:my_dict[0],reverse=False)
    # 关闭数据库连接
    cursor.close()
    conn.close()
    # 距离公式，a^2 + b^2，排序
    if(flag):
        return result[0][1] # 结果
    else:
        return None

# 扩大范围-->1性质扩大
def expand_range_plus_one(list_of_range):
    if(list_of_range[0] == 0):
        pass
    else:
        list_of_range[0] = list_of_range[0] - 1
    if(list_of_range[1] == 1000):
        pass
    else:
        list_of_range[1] = list_of_range[1] + 1
    if(list_of_range[2] == 0):
        pass
    else:
        list_of_range[2] = list_of_range[2] - 1
    if(list_of_range[3] == 1000):
        pass
    else:
        list_of_range[3] = list_of_range[3] + 1
    return list_of_range

# 扩大范围-->根号2倍数（按1.5倍数处理）
def expand_range_times_sqrt2(list_of_range):
    x_range = list_of_range[1] - list_of_range[0]
    y_range = list_of_range[3] - list_of_range[2]
    # 尽量把数据控制在0~1000的区间内，结果进行一定的处理
    # x_limit_l
    if(list_of_range[0] >= x_range*1.5/2): 
        list_of_range[0] = int(list_of_range[0] - x_range*1.5/2) #向下取整
    else:
        list_of_range[0] = 0
    # x_limit_r
    list_of_range[1] = math.ceil(list_of_range[1] + x_range*1.5/2) #向上取整
    if(list_of_range[1] > 1000):
        list_of_range[1] = 1000
    # y_limit_l
    if(list_of_range[2] >= y_range*1.5/2):
        list_of_range[2] = int(list_of_range[2] - y_range*1.5/2)
    else:
        list_of_range[2]= 0
    # y_limit_r
    list_of_range[3] = math.ceil(list_of_range[3] + y_range*1.5/2)
    if(list_of_range[3] >= 1000):
        list_of_range[3] = 1000
    return list_of_range
    