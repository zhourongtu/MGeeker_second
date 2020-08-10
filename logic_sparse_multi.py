import sparse_multi

# 1.数据存储接口
# sparse_multi.user_info_interface()

# 2.业务员接口
def test_nearest_priciple():
    yewu_number = input('请输入你指定的业务员坐标个数：')
    yewu_number = int(yewu_number)
    list_of_locs = []
    for i in range(yewu_number):
        my_str = input('请输入业务员{}的坐标（以空格键分开）：'.format(i+1))
        my_str = my_str.split(' ')
        list_of_locs.append([float(my_str[0]), float(my_str[1])])
    sparse_multi.yewuyuan_info_interface(list_of_locs)
test_nearest_priciple()