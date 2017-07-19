#from TradeBroker import TradeBroker
#from SPYTradeBroker import SPYTradeBroker
from RSIAlgorithm import RSIAlgorithm
from RSIAlgorithm2 import RSIAlgorithm2
from RSIAlgorithm3 import RSIAlgorithm3
from RSIAlgorithm4 import RSIAlgorithm4
from RSIAlgorithm5 import RSIAlgorithm5
from RSIAlgorithm6 import RSIAlgorithm6
from RSIAlgorithm8 import RSIAlgorithm8
from Algorithm import Algorithm
#from MatPlotDisplay import MatPlotDisplay
#from PlotlyDisplay import PlotlyDisplay
#from MatPlotStockDisplay import MatPlotStockDisplay
#from MatPlotStockDisplay2 import MatPlotStockDisplay2
#from MatPlotSubDisplay import MatPlotSubDisplay
import os

import csv

#from IGTradeBroker import IGTradeBroker
from IGTradeBrokerND import IGTradeBrokerND

#default_path='C:\\Users\\ktcm2\\Documents\\python\\stockTrading\\stockTrade(OO)'
#os.chdir(default_path)


data=[]


    
    
#with open('EURCHF_m5_Bid.csv', 'rt') as f:
#with open('SPYData28Mar2017.csv', 'rt') as f:
#    reader = csv.reader(f)
#    next(reader)
#    for date, time, Open, high, low, close, tTicks in reader:
#        tempRow={}
#        tempRow['Date']=date
#        tempRow['Time']=time
#        tempRow['Open']=Open
#        tempRow['High']=high
#        tempRow['Low']=low
#        tempRow['Close']=close
        #tempRow['Ticks']=tTicks
#        data.append(tempRow)

#rsiAlgorithm=RSIAlgorithm(intervalMin=5)
#rsiAlgorithm=RSIAlgorithm2(intervalMin=5)
#rsiAlgorithm=RSIAlgorithm3(intervalMin=5)
#rsiAlgorithm=RSIAlgorithm4(intervalMin=5)
#rsiAlgorithm=RSIAlgorithm5(intervalMin=5)
#rsiAlgorithm=RSIAlgorithm6(intervalMin=5)
rsiAlgorithm=RSIAlgorithm8(intervalMin=5)
#display=MatPlotStockDisplay()
#display=MatPlotStockDisplay2()
#display = MatPlotSubDisplay()
#display=MatPlotDisplay()
#display=PlotlyDisplay()
#myBroker = SPYTradeBroker(data = data, totalMoney=11000, invest=10000, algorithm = rsiAlgorithm, display=display)

#myBroker = IGTradeBroker(totalMoney=11000, invest=10000, algorithm = rsiAlgorithm, display=display)
print('Start')
myBroker = IGTradeBrokerND(totalMoney=11000, invest=10000, algorithm = rsiAlgorithm)
#myBroker.placePosition(True)

myBroker.trade()