import matplotlib.pyplot as plt
from Display import Display

class MatPlotDisplay (Display):
    def __init__(self):
        print('Init')
        
    def display(self, arr, anno):
        ax1 = plt.subplot2grid((1,1), (0,0))
        font_dict = {'family':'serif',
                 'color':'darkred',
                 'size':15}
        for i in range(0, len(arr)):
            ax1.text(i, arr[i]+2,anno[i], fontdict=font_dict)
        plt.plot(arr)
        plt.show()