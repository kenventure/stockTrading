# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 23:38:45 2017

@author: tham
"""

import json
from pprint import pprint

with open('data10Apr17.txt') as data_file:    
    data = json.load(data_file)

pprint(data)



print (data["prices"][0]["snapshotTime"])

print (data["prices"][1]["snapshotTime"])

print (len(data["prices"]))



totalMoney = 10000.00 #in dollars
totalAssets = 0
totalLots=0
for i in range (0, len(data["prices"])):
    print (data["prices"][i]["snapshotTime"])
    #print (data["prices"][i]["closePrice"]["bid"])
    bidPrice = data["prices"][i]["closePrice"]["bid"]
    print (bidPrice)
    buyAmount=0.00
    buyLots=2#negative for sell
    #insert your algorithm here
    buyAmount=buyLots * bidPrice
    totalLots=totalLots+buyLots
    totalAssets=totalLots*bidPrice
    #end
    totalMoney=totalMoney-buyAmount
    
    
print('Total Money {0}'.format(totalMoney))

print('Total Assets {0}'.format(totalAssets))

total = totalMoney + totalAssets

print('Total {0}'.format(total))