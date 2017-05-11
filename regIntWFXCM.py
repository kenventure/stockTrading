# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:22:16 2017

@author: tham
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 23:38:45 2017

@author: tham
"""

import json

import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
import os

import csv

def basic_linear_regression(x, y):
    # Basic computations to save a little time.
    
    if len(x)> 0:
        
        length = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
    
        # Σx^2, and Σxy respectively.
        sum_x_squared = sum(map(lambda a: a * a, x))
        sum_of_products = sum([x[i] * y[i] for i in range(length)])
    
        # Magic formulae!
        a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
        b = (sum_y - a * sum_x) / length
    else:
        a=0
        b=0
    return a, b


default_path='C:\\Users\\ktcm2\\Documents\\python\\stockTrading\\'
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
        




print (data[0])
print (len(data))


invest=10000
totalMoney = 11000.00 #in dollars
totalAssets = 0
totalLots=0

average = 0

sumStocks = 0
totalTrades = 0;

lastPrice = 0;

bought = False

xVals = []
yVals = []

firstBuy=False

timeFirstBuy=""


buySellPrice = float(data[0]["Close"])

totalMonVec = []

xVec=[]

totalEq = totalMoney
boughtLots=0
amtVec=[]
buyVec=[]
sellVec=[]
entryPrice=0
stopLossPrice=0

buyNum=2
sellNum=15
stopLossVal=10
numSell=0
numStopLoss=0
sellPrice=0.0
for i in range (0, 150000):

    
    isBuy = False
    isSell = False
    bidPrice = float(data[i]["Close"])
    

    

    buyAmount=0.00
    buyLots=0
    
    valueInterest=bidPrice


    
    if len(xVals)>1000:  
        xVals.pop(0)
        yVals.pop(0)
        
        xCut = xVals[:999]
        yCut = yVals[:999]
        regression = np.polyfit(xCut, yCut, 1)
        #print('Regression a {0} b {1} Time {2}'.format(regression[0], regression[1], data["prices"][i]["snapshotTime"]))
        valueInterest = regression[0]*i + regression[1]
        #print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
        if bidPrice > (sellPrice) and bought==True:
            #buyLots=-10000#negative for sell
            
            #print ('Intend Sell')
            #print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
            isSell = True
            numSell=numSell+1
        else:
            if (valueInterest-buyNum*np.std(yCut)) > bidPrice and bought==False:
                #buyLots=10000
                #print('Intend buy')
                #print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
                isBuy=True
            
        
#        if bought==False:
#            if bidPrice > (valueInterest+ 10*np.std(yCut)):
#                #buyLots=10000
#                isBuy = True
#        else:
#            if bidPrice < (valueInterest- 10*np.std(yCut)):
#                #buyLots=-10000
#                isSell = True
        
    
    #insert your algorithm here
    buyAmount=buyLots * bidPrice
   # print ('Buy amount {0} TOtal lots {1}'.format(buyAmount, totalLots))    
   # n = bidPrice
   # fstr = repr(n)
   # signif_digits, fract_digits = fstr.split('.')
    # >  ['179', '123']
   # fract_lastdigit = int(fract_digits[-1])
    # >  9
   # pic = float(fract_lastdigit)
   # pic = pic / 100000    
    pic=0.0001
    #tradeFee = pic * buyLots
    
    #print ('Average {0} 
   # print('Bid Price {1}'.format(average, bidPrice))
    
    if bought==True and bidPrice < stopLossPrice: # stop loss
        isSell=True
        print ('Stop loss')
        numStopLoss=numStopLoss+1
    #print ('Pic {0}, Trade Fee: {1}'.format(pic, tradeFee))
    if isBuy==True:
    #if buyAmount > 0:
        amtVec.append(0)
        if  bought == False:
            boughtLots=invest/bidPrice
            tradeFee=pic * boughtLots
            if (tradeFee<=(totalMoney-invest)):
                totalMoney=totalMoney-tradeFee-invest
                totalTrades = totalTrades + 1
                print ('Buy  Date {0} Time {1}'.format(data[i]['Date'], data[i]['Time']))
                bought = True
                entryPrice=bidPrice
                stopLossPrice=entryPrice-stopLossVal*pic
                sellPrice=entryPrice+sellNum*pic
                timeFirstBuy =  data[i]["Time"]
                print ('valueInterest {0} Bid Price {1}'.format(valueInterest, bidPrice))
                buyVec.append(bidPrice)
           # isBuy=True
            buySellPrice=bidPrice
    else:
        #if buyAmount<0 and bought == True:
        if isSell == True:
            #if (abs(buyLots)<=totalLots) and (tradeFee<=totalMoney):
            if (tradeFee<=(totalMoney)):
                tradeFee=pic * boughtLots
                amount=bidPrice*boughtLots
                totalMoney=totalMoney-tradeFee+amount
                totalTrades = totalTrades + 1
                print ('Sell  Date {0} Time {1}'.format(data[i]['Date'], data[i]['Time']))
                print ('valueInterest {0} Bid Price {1}'.format(valueInterest, bidPrice))
                bought = False
             #   isBuy=False
                amtVec.append(amount)
                buySellPrice=bidPrice
                sellVec.append(bidPrice)
            else:
               # print ('Cannot sell as sell conditions not met')
                amtVec.append(0)
        else:
            amtVec.append(0)
    #totalCash = totalMoney + totalAssets
    if bought==True:
        totalEq=totalMoney+bidPrice*boughtLots
    else:
        totalEq=totalMoney
    totalMonVec.append(totalEq)
    xVec.append(i)
    xVals.append(i)
    yVals.append(bidPrice)
    lastPrice = bidPrice


	
	
 
    
df = pd.DataFrame(totalMonVec)
#df = df.cumsum() 
df.plot()

##df2=pd.DataFrame(amtVec)
##df2.plot()
##
##df3=pd.DataFrame(buyVec)
##
##df3.plot()
##
##df4=pd.DataFrame(sellVec)
##df4.plot()
#plt.ion()
plt.show()
print('Total Equity {0}'.format(totalEq))

print ('Total Trades {0}, Buy {1} Sell {2}'.format(totalTrades, len(buyVec), len(sellVec)))

print ('Mean buy{0}, Mean sell {1}'.format(np.mean(buyVec), np.mean(sellVec)))

print ('Num sell {0}, Num stop loss {1}'.format(numSell, numStopLoss))


