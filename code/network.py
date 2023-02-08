import pickle, base64
from layer import Layer
import numpy as np
from time import time

class Network:
    def __init__(self, layers_len: list, activations: list, activations_derivs: list, load=False,filename=None) -> None:
        if not load:
            self.layers = []
            for i in range(len(layers_len) - 1):
                layer = Layer(layers_len[i], layers_len[i+1],
                            activations[i], activations_derivs[i])
                self.layers.append(layer)
        else:
            with open(filename,'r') as f:
                self.layers = pickle.loads(base64.b64decode(f.read().encode()))
            

    def calc_cost(self, input_array, target_array):
        output = self.predict(input_array)
        return np.sum(np.square(output - (target_array)))

    def train(self, x_train, y_train, learning_rate, cost_to_stop=0.001):
        total_cost = 1
        min_cost = 1
        length = len(x_train)
        times = 0

        while total_cost > cost_to_stop:
            total_cost = 0
            for i, input_array in enumerate(x_train):
                target = y_train[i]

                output = input_array
                outputs = []
                for layer in self.layers:
                    outputs.append(output)
                    output = layer.forward_propagation(output)

                for j, layer in enumerate(reversed(self.layers)):
                    target = layer.backward_propagation(
                        outputs[-j-1], target, learning_rate)

                total_cost += self.calc_cost(input_array, y_train[i])

            total_cost /= length
            learning_rate = total_cost / 1.5
            times += 1

            if total_cost< min_cost:
                min_cost = total_cost
                self.save()

            print(f"{times} times | total cost: {total_cost} | learning rate: {learning_rate}")

    def predict(self, input_array):
        for layer in self.layers:
            input_array = layer.forward_propagation(input_array)
        return input_array

    def save(self):
        with open(f'nets\\layers_{time()}.net','w') as f:
            f.write(base64.b64encode(pickle.dumps(self.layers)).decode())
