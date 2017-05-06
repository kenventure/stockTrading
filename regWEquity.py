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
#from pprint import pprint
#from ggplot import *
#import matplotlib.pyplot as plt
import pandas as pd
import os
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


default_path='C:\\Users\\tham\\Documents\\python\\stockTrading\\stockTrading\\'
os.chdir(default_path)


#with open('dataMar.txt') as data_file:    
#with open('20Feb17.txt') as data_file:    
with open('1Mar14Mar.txt') as data_file:    
    data = json.load(data_file)

#with open ('20Mar25Mar.txt') as data_file:
  #  data2 = json.load(data_file)
    
#data = dict(data1.items() + data2.items())
#pprint(data)



print (data["prices"][0]["snapshotTime"])

print (data["prices"][1]["snapshotTime"])

print (len(data["prices"]))


invest=10000
totalMoney = 11000.00 #in dollars
totalAssets = 0
totalLots=0
print (len(data["prices"]))

average = 0

sumStocks = 0
totalTrades = 0;

lastPrice = 0;

bought = False

xVals = []
yVals = []

firstBuy=False

timeFirstBuy=""


buySellPrice = data["prices"][0]["closePrice"]["bid"]

totalMonVec = []

xVec=[]

totalEq = totalMoney
boughtLots=0
amtVec=[]
buyVec=[]
sellVec=[]
entryPrice=0
stopLossPrice=0
for i in range (0, len(data["prices"])):
    #print (data["prices"][i]["snapshotTime"])
    #print (data["prices"][i]["closePrice"]["bid"])
    
    isBuy = False
    isSell = False
    bidPrice = data["prices"][i]["closePrice"]["bid"]
    

    
   # a, b = basic_linear_regression(xVals, yVals)
   
    
    #sumStocks = sumStocks + bidPrice
    
    #average = sumStocks / (i+1)
    
    
    #print (bidPrice)
    buyAmount=0.00
    buyLots=0
    
    valueInterest=bidPrice
    
    if len(xVals)>50:  
        xVals.pop(0)
        yVals.pop(0)
        
        xCut = xVals[:49]
        yCut = yVals[:49]
        regression = np.polyfit(xCut, yCut, 1)
        #print('Regression a {0} b {1} Time {2}'.format(regression[0], regression[1], data["prices"][i]["snapshotTime"]))
        valueInterest = regression[0]*i + regression[1]
        #print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
        if bidPrice > (valueInterest+ 10.0*np.std(yCut)) and bought==True:
            #buyLots=-10000#negative for sell
            
            #print ('Intend Sell')
            #print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
            isSell = True
        else:
            if (valueInterest-1.0*np.std(yCut)) > bidPrice and bought==False:
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
    
    n = bidPrice
    fstr = repr(n)
    signif_digits, fract_digits = fstr.split('.')
    # >  ['179', '123']
    fract_lastdigit = int(fract_digits[-1])
    # >  9
    pic = float(fract_lastdigit)
    pic = pic / 100000
    #tradeFee = pic * buyLots
    
    #print ('Average {0} 
   # print('Bid Price {1}'.format(average, bidPrice))
    
    if bought==True and bidPrice < stopLossPrice: # stop loss
        isSell=True
    #print ('Pic {0}, Trade Fee: {1}'.format(pic, tradeFee))
    if isBuy==True:
    #if buyAmount > 0:
        amtVec.append(0)
        if  bought == False:
            boughtLots=invest/bidPrice
            tradeFee=pic * boughtLots
            if (tradeFee<=(totalEq-invest)):
                totalEq=totalEq-tradeFee
                totalTrades = totalTrades + 1
                print ('Buy  Time {0}'.format(data["prices"][i]["snapshotTime"]))
                bought = True
                entryPrice=bidPrice
                stopLossPrice=entryPrice-10*pic
                timeFirstBuy =  data["prices"][i]["snapshotTime"]
                print ('valueInterest {0} Bid Price {1}'.format(valueInterest, bidPrice))
                buyVec.append(bidPrice)
           # isBuy=True
            buySellPrice=bidPrice
    else:
        #if buyAmount<0 and bought == True:
        if isSell == True:
            #if (abs(buyLots)<=totalLots) and (tradeFee<=totalMoney):
            if (tradeFee<=(totalEq-invest)):
                tradeFee=pic * boughtLots
                amount=bidPrice*boughtLots
                totalEq=totalEq-invest+amount-tradeFee
                totalTrades = totalTrades + 1
                print ('Sell {0} Time {1}'.format (abs(amount), data["prices"][i]["snapshotTime"]))
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
    totalMonVec.append(totalEq)
    xVec.append(i)
    xVals.append(i)
    yVals.append(bidPrice)
    lastPrice = bidPrice
 
    
df = pd.DataFrame(totalMonVec)
#df = df.cumsum() 
df.plot()

df2=pd.DataFrame(amtVec)
df2.plot()

df3=pd.DataFrame(buyVec)

df3.plot()

df4=pd.DataFrame(sellVec)
df4.plot()
print('Total Equity {0}'.format(totalEq))

print ('Total Trades {0}, Buy {1} Sell {2}'.format(totalTrades, len(buyVec), len(sellVec)))

print ('Mean buy{0}, Mean sell {1}'.format(np.mean(buyVec), np.mean(sellVec)))
