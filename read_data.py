import pymysql
conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '123456',
    db = 'test',
    charset = 'utf8'
)
cursor = conn.cursor()
f = open('data.txt', 'r')
datas = f.readlines()
i = 0
for data in datas:
    data = data.split(',')
    id = int(data[0])
    x_loc = round(float(data[1]), 2)
    y_loc = round(float(data[2]), 2)
    x_block = int(x_loc)
    y_block = int(y_loc)
    sql = 'INSERT INTO user_info VALUES({0}, {1}, {2}, {3}, {4});'.format(id, x_loc, y_loc, x_block, y_block)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        i = i+1
    except:
        # 发生错误时回滚
        conn.rollback()
    if(i % 1000 == 0):
        conn.commit()
        print(i/1000)
    if(i % 10000 == 0):
        print(i/10000)

conn.commit()
cursor.close()
conn.close()