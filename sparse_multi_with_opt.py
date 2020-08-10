import pymysql
import random
# 初始化城市，修改后-->初始化用户坐标
def xy():
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
    # 此时datas为所有用户的数据
    li = []
    
    # 这里是业务员地址
    yewu_number = input('请输入你指定的业务员坐标个数：')
    yewu_number = int(yewu_number)
    for i in range(yewu_number):
        my_str = input('请输入业务员{}的坐标（以空格键分开）：'.format(i+1))
        my_str = my_str.split(' ')
        li.append([float(my_str[0]), float(my_str[1])])
    if(yewu_number < 10):
        for i in range(10 - yewu_number):
            li.append([round(random.random() * 1000, 2), round(random.random() * 1000, 2)])
    
    for data in datas:
        li.append([float(data[1]), float(data[2])])
    
    # 按特定index排列
    my_index = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 24]
    
    li = np.array(li)
    # return np.array(
    #     [[100, 200], [234, 1245], [423, 124], [123, 974], [578, 294], [1000, 500], [492, 2100], [320, 418], [836, 914]])
    return li

def D(location1, location2):
    return math.sqrt(pow(location1[0] - location2[0], 2) + pow(location1[1] - location2[1], 2))
    
def DMAT(locations):
    length = len(locations)
    distance = np.ones([length, length])
    # print(distance.shape)
    for i in range(length):
        for j in range(length):
            distance[i, j] = D(locations[i], locations[j])
    return distance


def init_population(length, num):
    li = list(range(length))
    print(li)
    population = []
    for i in range(num):
        random.shuffle(li)
        population.append(copy.deepcopy(li))
    return population


def aimFunction(entity, DMAT, break_points):
    """
    目标函数
    :param entity: 个体
    :param DMAT: 距离矩阵
    :param break_points: 切断点
    :return:
    """
    distance = 0
    break_points.insert(0, 0)
    break_points.append(len(entity))
    routes = []
    for i in range(len(break_points) - 1):
        routes.append(entity[break_points[i]:break_points[i + 1]])
    # print(routes)
    for route in routes:
        route.append(route[0])
        for i in range(len(route)-1):
            distance += DMAT[route[i],route[i+1]]

    return 1.0/distance


def fitness(population, DMAT, break_points, aimFunction):
    """
    适应度
    :param population: 种群
    :param DMAT: 距离矩阵
    :param break_points:切断点
    :param aimFunction: 目标函数
    :return:
    """

    value = []
    for i in range(len(population)):
        value.append(aimFunction(population[i], DMAT, copy.deepcopy(break_points)))
        # weed out negative value
        if value[i] < 0:
            value[i] = 0
    return value


def selection(population, value):
    # 轮盘赌选择
    fitness_sum = []
    for i in range(len(value)):
        if i == 0:
            fitness_sum.append(value[i])
        else:
            fitness_sum.append(fitness_sum[i - 1] + value[i])

    for i in range(len(fitness_sum)):
        fitness_sum[i] /= sum(value)

    # select new population
    population_new = []
    for i in range(len(value)):
        rand = np.random.uniform(0, 1)
        for j in range(len(value)):
            if j == 0:
                if 0 < rand and rand <= fitness_sum[j]:
                    population_new.append(population[j])

            else:
                if fitness_sum[j - 1] < rand and rand <= fitness_sum[j]:
                    population_new.append(population[j])
    return population_new


def amend(entity, low, high):
    """
    修正个体
    :param entity: 个体
    :param low: 交叉点最低处
    :param high: 交叉点最高处
    :return:
    """
    length = len(entity)
    cross_gene = entity[low:high]  # 交叉基因
    not_in_cross = []  # 应交叉基因
    raw = entity[0:low] + entity[high:]  # 非交叉基因


    for i in range(length):
        if not i in cross_gene:
            not_in_cross.append(i)

    error_index = []
    for i in range(len(raw)):
        if raw[i] in not_in_cross:
            not_in_cross.remove(raw[i])
        else:
            error_index.append(i)
    for i in range(len(error_index)):
        raw[error_index[i]] = not_in_cross[i]

    entity = raw[0:low] + cross_gene + raw[low:]

    return entity


def crossover(population_new, pc):
    """
    交叉
    :param population_new: 种群
    :param pc: 交叉概率
    :return:
    """
    half = int(len(population_new) / 2)
    father = population_new[:half]
    mother = population_new[half:]
    np.random.shuffle(father)
    np.random.shuffle(mother)
    offspring = []
    for i in range(half):
        if np.random.uniform(0, 1) <= pc:
            # cut1 = np.random.randint(0, len(population_new[0]))
            # if cut1 >len(father[i]) -5:
            #     cut2 = cut1-5
            # else:
            #     cut2 = cut1+5
            cut1 = 0
            cut2 = np.random.randint(0, len(population_new[0]))
            if cut1 > cut2:
                cut1, cut2 = cut2, cut1
            if cut1 == cut2:
                son = father[i]
                daughter = mother[i]
            else:
                son = father[i][0:cut1] + mother[i][cut1:cut2] + father[i][cut2:]
                son = amend(son, cut1, cut2)
                daughter = mother[i][0:cut1] + father[i][cut1:cut2] + mother[i][cut2:]
                daughter = amend(daughter, cut1, cut2)

        else:
            son = father[i]
            daughter = mother[i]
        offspring.append(son)
        offspring.append(daughter)

    return offspring


def mutation(offspring, pm):
    for i in range(len(offspring)):
        if np.random.uniform(0, 1) <= pm:
            position1 = np.random.randint(0, len(offspring[i]))
            position2 = np.random.randint(0, len(offspring[i]))
            # print(offspring[i])
            offspring[i][position1],offspring[i][position2] = offspring[i][position2],offspring[i][position1]
            # print(offspring[i])
    return offspring

import numpy as np
from matplotlib import pyplot as plt
import math
import copy
import random

def show_population(population):
    # x = [i / 100 for i in range(900)]
    x = [i / 100 for i in range(-450, 450)]
    y = [0 for i in range(900)]
    for i in range(900):
        y[i] = aimFunction(x[i])

    population_10 = [decode(p) for p in population]
    y_population = [aimFunction(p) for p in population_10]

    plt.plot(x, y)
    plt.plot(population_10, y_population, 'ro')
    plt.show()


if __name__ == '__main__':

    # x = [i / 100 for i in range(900)]
    # y = [0 for i in range(900)]

    locations = xy()
    DMAT = DMAT(locations)
    break_points = [2, 4, 6, 8, 10, 12, 14, 16, 18]
#     break_points = [0, 3, 6, 24]
#     break_points = [6, 10, 16, 24]
    population = init_population(len(locations), 90)

    t = []
    for i in range(4001):
        # selection
        value = fitness(population, DMAT, break_points, aimFunction)
        population_new = selection(population, value)
        # crossover
        offspring = crossover(population_new, 0.65)
        # mutation
        population = mutation(offspring, 0.02)
        # if i % 1 == 0:
        #     show_population(population)
        result = []
        for j in range(len(population)):
            result.append(1.0 / aimFunction(population[j], DMAT, copy.deepcopy(break_points)))

        t.append(min(result))
        if i % 400 == 0:
            min_entity = population[result.index(min(result))]
            plt.scatter(locations[:, 0], locations[:, 1])

            routes = []
            break_points_plt = copy.deepcopy(break_points)
            break_points_plt.insert(0, 0)
            break_points_plt.append(len(min_entity))
            for i in range(len(break_points_plt) - 1):
                routes.append(min_entity[break_points_plt[i]:break_points_plt[i + 1]])
            for route in routes:
                route.append(route[0])
            for route in routes:
                x = locations[route, 0]
                y = locations[route, 1]
                plt.plot(x, y)

            plt.show()

        # print(min(result))

    print(t)
    plt.plot(t)
    # plt.axhline(max(y), linewidth=1, color='r')
    plt.show()

