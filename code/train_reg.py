from network import Network
from activations import *
from SQL_ORM import DotORM
import numpy as np
from time import time



def create_network():
    return Network([3,9,27,81,81,81,27,9,3,1],9*[sigmoid],9*[sigmoid_deriv])

def load_network():
    return Network(0,0,0,True,'nets\\20_times')


def start():
    network = create_network()

    train_obj = Train(network)

    train_obj.train('yoavmosseri',0.0001)

    train_obj.save()



class Train:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.db = DotORM()

    def __normalize_data(self, data):
        column_1 = data[:,0] 
        column_1 = (column_1 - column_1.min()) / (column_1.max() - column_1.min())

        column_2 = data[:,1] 
        column_2 = (column_2 - column_2.min()) / (column_2.max() - column_2.min())

        column_3 = data[:,2] 
        column_3 = (column_3 - column_3.min()) / (column_3.max() - column_3.min())

        return np.stack((column_1, column_2, column_3), axis=1)

    def train(self, username, cost_to_stop=0.01):
        data = self.__generate_data(username)
        print('>>>>>>>>>>>>>>>>\t\tTraining Started\t\t<<<<<<<<<<<<<<<<')
        start_time = time()
        self.network.train(data,np.ones(len(data)),0.1,cost_to_stop)
        end_time = time()
        print(f'>>>>>>>>>>>>>>>>\tTraining Ended after {int((end_time-start_time)/60)} minutes\t\t<<<<<<<<<<<<<<<<')


    def __generate_data(self, username):
        my_data_x = self.db.get_user_data(username)
        my_data_x = self.__normalize_data(my_data_x)

        return my_data_x

    def save(self):
        self.network.save()








start()