import multi_thread

def logic_multi_thread():
    yewu_number = input('请输入你指定的业务员坐标个数：')
    yewu_number = int(yewu_number)
    list_of_locs = []
    for i in range(yewu_number):
        my_str = input('请输入业务员{}的坐标（以空格键分开）：'.format(i+1))
        my_str = my_str.split(' ')
        list_of_locs.append([float(my_str[0]), float(my_str[1])])
    multi_thread.multi_yewu(list_of_locs)

logic_multi_thread()