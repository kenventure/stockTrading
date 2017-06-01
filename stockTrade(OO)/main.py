from TradeBroker import TradeBroker
from RSIAlgorithm import RSIAlgorithm
from Algorithm import Algorithm
from MatPlotDisplay import MatPlotDisplay
from PlotlyDisplay import PlotlyDisplay
from MatPlotStockDisplay import MatPlotStockDisplay
import os

import csv

default_path='C:\\Users\\ktcm2\\Documents\\python\\stockTrading\\stockTrade(OO)'
os.chdir(default_path)


data=[]

with open('EURCHF_m5_Bid.csv', 'rt') as f:
    reader = csv.reader(f)
    next(reader)
    for date, time, Open, high, low, close, tTicks in reader:
        tempRow={}
        tempRow['Date']=date
        tempRow['Time']=time
        tempRow['Open']=Open
        tempRow['High']=high
        tempRow['Low']=low
        tempRow['Close']=close
        tempRow['Ticks']=tTicks
        data.append(tempRow)

rsiAlgorithm=RSIAlgorithm(intervalMin=5)
display=MatPlotStockDisplay()
#display=MatPlotDisplay()
#display=PlotlyDisplay()
myBroker = TradeBroker(data = data, totalMoney=11000, invest=10000, algorithm = rsiAlgorithm, display=display)

myBroker.trade()