from network import Network
import numpy as np
from SQL_ORM import DotORM
import matplotlib.pyplot as plt
from plot import Graph
import random
db = DotORM()

def normalize_data(data):
    column_1 = data[:,0] 
    column_1 = (column_1 - column_1.min()) / (column_1.max() - column_1.min())

    column_2 = data[:,1] 
    column_2 = (column_2 - column_2.min()) / (column_2.max() - column_2.min())

    column_3 = data[:,2] 
    column_3 = (column_3 - column_3.min()) / (column_3.max() - column_3.min())

    return np.stack((column_1, column_2, column_3), axis=1)


def generate_data(username):
    my_data_x = db.get_user_data(username)
    my_data_x = normalize_data(my_data_x)

    return my_data_x


def get_cost_list(network: Network,data: list) -> list:
    cost_lst = []
    for item in data:
        cost_lst.append(network.calc_cost(item,item))

    return cost_lst


def get_limit_cost(network: Network,data: list) -> float:
    cost_sum = 0
    cnt = 0

    for item in data:
        cost = network.calc_cost(item,item)
        cost_sum += cost
        cnt+=1

    return cost_sum / cnt






network = Network(0,0,0,True,"nets\\50_times.net")

data  = generate_data('yoavmosseri')

g = Graph()

g(get_cost_list(network, data))

exit()


data = generate_data('yoavmosseri')


print('loaded')

list_of_all_costs = []
cost_sum = 0
cnt = 0


for item in data:
    cost = network.calc_cost(item,item)
    list_of_all_costs.append(cost)
    cost_sum += cost
    cnt+=1

cost_avg = cost_sum / cnt

print(f"Costs sum = {cost_sum}.")
print(f"{cnt} items.")
print(f"Cost average = {cost_avg}.")
print(get_limit_cost(network,'yoavmosseri'))









exit()
