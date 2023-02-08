import matplotlib.pyplot as plt


class Graph:
        def __init__(self, name="My graph",xlabel="X" ,ylabel="How many", color='purple') -> None:
                plt.title(name)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                self.color = color

        def   __call__(self, list_of_data):
            self.insert_data(list_of_data,end=0.05,bins=100)
            self.show()
                

        def insert_data(self, list_of_data:list, start:int =0,end :int=None, bins:int=10):
                range = (start, end if end is not None else max(list_of_data))
                print(range)
                plt.hist(list_of_data,bins,range,color= self.color,histtype = 'bar',rwidth=2)

        def show(self):
                plt.show()

        def close(self):
                plt.close()
        

