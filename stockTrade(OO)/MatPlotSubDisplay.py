import datetime
import numpy as np
import matplotlib.colors as colors
import mpl_finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from Display import Display

class MatPlotSubDisplay (Display):
    def __init__(self):
        print('Init')
        
    def display(self, arr, anno, price):
        buyVec=[]
        sellVec=[]
        for i in range(0, len(anno)):
            if anno[i] is 'b':
                buyVec.append(100)
            else:
                buyVec.append(0)
        for i in range(0, len(anno)):
            if anno[i] is 's':
                sellVec.append(100)
            else:
                sellVec.append(0)
                
        plt.rc('axes', grid=True)
        plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
        textsize = 9
        #left, width = 0.1, 0.8
        #rect1 = [left, 0.7, width, 0.3]
        #rect2 = [left, 0.35, width, 0.3]
        #rect3 = [left, 0.2, width, 0.1]
        #rect4 = [left, 0.05, width, 0.1]
        
        fig = plt.figure(facecolor='white')
        axescolor = '#f6f6f6'  # the axes background color
        fillcolor = 'darkgoldenrod'
        ax1 = plt.subplot(4,1,1)  # left, bottom, width, height
        ax1.plot(arr, color=fillcolor)
        ax1.text(0.025, 0.95, 'Equity', va='top', transform=ax1.transAxes, fontsize=textsize)

        ax2 = plt.subplot(4,1,2)  # left, bottom, width, height
        ax2.yaxis.set_ticks(np.arange(0.9, 1.3, 0.001))
        ax2.plot(price, color=fillcolor)
        ax2.text(0.025, 0.95, 'Bid Price', va='top', transform=ax2.transAxes, fontsize=textsize)
        ax3 = plt.subplot(4,1,3)  # left, bottom, width, height
        ax3.plot(buyVec, color='red')        
        ax3.text(0.025, 0.95, 'Buy', va='top', transform=ax3.transAxes, fontsize=textsize)
        ax4 = plt.subplot(4,1,4)  # left, bottom, width, height
        ax4.plot(sellVec, color='green')        
        ax4.text(0.025, 0.95, 'Sell', va='top', transform=ax4.transAxes, fontsize=textsize)
        plt.show()
        

    def log(self, arr, anno, price):
        target = open('output.csv','w')
        target.write("Index,Equity,BuySell,Price]\n")
        for i in range(0, len(arr)):
            str1=""
            str1=str(i)+","+str(arr[i])+","+anno[i]+","+str(price[i])+"\n"
            target.write(str1)
        target.close()