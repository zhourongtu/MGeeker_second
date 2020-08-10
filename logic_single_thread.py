import single_thread

def logic_single_thread():
    my_str = input("请输入业务员的坐标（以空格键分开）:")
    my_str = my_str.split(' ')
    result = single_thread.query_nearest(float(my_str[0]), float(my_str[1]))
    print('用户编号：', result[0], '用户坐标：x ', result[1], ', y ', result[2])
logic_single_thread()