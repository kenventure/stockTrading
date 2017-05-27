import matplotlib.pyplot as plt
from Display import Display

class MatPlotDisplay (Display):
    def __init__(self):
        print('Init')
        
    def display(self, arr, anno):
        plt.plot(arr)
        plt.show()