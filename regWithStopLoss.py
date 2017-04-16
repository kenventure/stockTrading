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


with open('dataMar.txt') as data_file:    
    data = json.load(data_file)

#with open ('20Mar25Mar.txt') as data_file:
  #  data2 = json.load(data_file)
    
#data = dict(data1.items() + data2.items())
#pprint(data)



print (data["prices"][0]["snapshotTime"])

print (data["prices"][1]["snapshotTime"])

print (len(data["prices"]))



totalMoney = 10000.00 #in dollars
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

isBuy = False
buySellPrice = data["prices"][0]["closePrice"]["bid"]

totalMonVec = []

xVec=[]
for i in range (0, len(data["prices"])):
    #print (data["prices"][i]["snapshotTime"])
    #print (data["prices"][i]["closePrice"]["bid"])
    
    
    bidPrice = data["prices"][i]["closePrice"]["bid"]
    

    
   # a, b = basic_linear_regression(xVals, yVals)
   
    
    #sumStocks = sumStocks + bidPrice
    
    #average = sumStocks / (i+1)
    
    
    #print (bidPrice)
    buyAmount=0.00
    buyLots=0
    
    valueInterest=bidPrice
    
    if len(xVals)>100:  
        xVals.pop(0)
        yVals.pop(0)
        
        xCut = xVals[:99]
        yCut = yVals[:99]
        regression = np.polyfit(xCut, yCut, 1)
        #print('Regression a {0} b {1} Time {2}'.format(regression[0], regression[1], data["prices"][i]["snapshotTime"]))
        valueInterest = regression[0]*i + regression[1]
        #print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
    if bidPrice > (valueInterest+ 1.0*np.std(yCut)):
        buyLots=-10000#negative for sell
        print ('Intend Sell')
        print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
    else:
        if (valueInterest-1.0*np.std(yCut)) > bidPrice:
            buyLots=10000
            print('Intend buy')
            print ('Value Interest {0} Bid Price {1}'.format(valueInterest, bidPrice))
            
        
    if bought==False:
        if bidPrice > (valueInterest+ 10*np.std(yCut)):
            buyLots=10000
    else:
        if bidPrice < (valueInterest- 10*np.std(yCut)):
            buyLots=-10000
    
    
    #insert your algorithm here
    buyAmount=buyLots * bidPrice
    print ('Buy amount {0} TOtal lots {1}'.format(buyAmount, totalLots))    
    
    n = bidPrice
    fstr = repr(n)
    signif_digits, fract_digits = fstr.split('.')
    # >  ['179', '123']
    fract_lastdigit = int(fract_digits[-1])
    # >  9
    pic = float(fract_lastdigit)
    pic = pic / 100000
    tradeFee = pic * buyLots
    
    #print ('Average {0} Bid Price {1}'.format(average, bidPrice))
    #print ('Pic {0}, Trade Fee: {1}'.format(pic, tradeFee))
    if buyAmount > 0:
    #if buyAmount > 0:
        if (buyAmount+tradeFee) <= totalMoney and bought == False:
            totalLots=totalLots+buyLots
            totalAssets=totalLots*bidPrice
        #end
            totalMoney=totalMoney-buyAmount-tradeFee
            totalTrades = totalTrades + 1
            print ('Buy {0} Time {1}'.format(buyAmount, data["prices"][i]["snapshotTime"]))
            bought = True
            timeFirstBuy =  data["prices"][i]["snapshotTime"]
            print ('valueInterest {0} Bid Price {1}'.format(valueInterest, bidPrice))
           # isBuy=True
            buySellPrice=bidPrice
    else:
        #if buyAmount<0 and bought == True:
        if buyAmount<0:
            #if (abs(buyLots)<=totalLots) and (tradeFee<=totalMoney):
            if (tradeFee<=totalMoney):
                totalLots=totalLots+buyLots
                totalAssets=totalLots*bidPrice
            #end
                totalMoney=totalMoney-buyAmount-tradeFee
                totalTrades = totalTrades + 1
                print ('Sell {0} Time {1}'.format (abs(buyAmount), data["prices"][i]["snapshotTime"]))
                print ('valueInterest {0} Bid Price {1}'.format(valueInterest, bidPrice))
                bought = False
             #   isBuy=False
                buySellPrice=bidPrice
            else:
                print ('Cannot sell as sell conditions not met')
    totalCash = totalMoney + totalAssets
    totalMonVec.append(totalCash)
    xVec.append(i)
    xVals.append(i)
    yVals.append(bidPrice)
    lastPrice = bidPrice
 
    
df = pd.DataFrame(totalMonVec)
#df = df.cumsum() 
df.plot()
totalMoney = lastPrice * totalLots + totalMoney
totalLots = 0
totalAssets=totalLots*lastPrice
print('Total Money {0}'.format(totalMoney))

print('Total Assets {0}'.format(totalAssets))

total = totalMoney + totalAssets
print ('Time first buy {0}'.format(timeFirstBuy))
print('Total {0}'.format(total))

print ('Total Trades {0}'.format(totalTrades))