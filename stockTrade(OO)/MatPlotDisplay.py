import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from Display import Display

class MatPlotDisplay (Display):
    def __init__(self):
        print('Init')
        
    def display(self, arr, anno, price):
        plt.figure(1)
        axcolor = 'lightgoldenrodyellow'
        

        plt.plot(arr)
        axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

        spos = Slider(axpos, 'Pos', 0.1, 90.0)
        plt.figure(2)
        ax1 = plt.subplot2grid((1,1), (0,0))
        font_dict = {'family':'serif',
                 'color':'darkred',
                 'size':10}
        #xArr=[]
        for i in range(0, len(arr)):
            ax1.text(i, price[i]+0.001,anno[i], fontdict=font_dict)
            #xArr.append(i)
        plt.plot(price)
        plt.show()
        
    def log(self, arr, anno, price):
        target = open('output.csv','w')
        target.write("Index,Equity,BuySell,Price]\n")
        for i in range(0, len(arr)):
            str1=""
            str1=str(i)+","+str(arr[i])+","+anno[i]+","+str(price[i])+"\n"
            target.write(str1)
        target.close()