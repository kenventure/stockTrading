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
from pprint import pprint

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

for i in range (0, len(data["prices"])):
    #print (data["prices"][i]["snapshotTime"])
    #print (data["prices"][i]["closePrice"]["bid"])
    bidPrice = data["prices"][i]["closePrice"]["bid"]
    
    sumStocks = sumStocks + bidPrice
    
    average = sumStocks / (i+1)
    
    
    #print (bidPrice)
    buyAmount=0.00
    buyLots=0
    
    if (bidPrice - average) > 0.013:
        buyLots=-30#negative for sell
    else:
        if (average - bidPrice) < 0.05:
            buyLots=30
        
    
        
    #insert your algorithm here
    buyAmount=buyLots * bidPrice
    
    if buyAmount > 0:
        if buyAmount < totalMoney:
            totalLots=totalLots+buyLots
            totalAssets=totalLots*bidPrice
        #end
            totalMoney=totalMoney-buyAmount
    else:
        if abs(buyLots)<totalLots:
            totalLots=totalLots+buyLots
            totalAssets=totalLots*bidPrice
        #end
            totalMoney=totalMoney-buyAmount
    
    
print('Total Money {0}'.format(totalMoney))

print('Total Assets {0}'.format(totalAssets))

total = totalMoney + totalAssets

print('Total {0}'.format(total))