from Algorithm import Algorithm
from datetime import datetime
import numpy as np

class GuardArr():
    def __init__(self, limit):
        self.array=[]
        self.limit=limit
        
    def insert(self, value):
        self.array.append(value)
        
        while (len(self.array)>self.limit):
            self.array= self.array[1:]
            
    def stdDev(self):
        return np.std(self.array)
        
        
class RSIAlgorithm8(Algorithm):
    def __init__(self, intervalMin):
        self.intervalMin = intervalMin
        self.isStart=True
        self.lastPrice=0
        self.gainlossVec=[]
        self.buyCondition = False
        self.sellCondition = False
        #self.conditionTime=datetime(2010, 9, 12, 11, 19, 54)
        self.sellPrice=0.0
        self.stopPrice = 0.0
        self.first = True
        self.prevAvgLoss = 0.0
        self.bought = False
        self.RSI=0
        self.RSIVec=[]
        self.B_RSILevel = 40
        self.sellRSI=69
        self.stopRSI=29
        self.S_RSILevel = 60
        self.buyRSI= 31
        self.buyStopRSI = 69
        self.condTime=0
        self.currTime=0
        self.isOpen=False
        self.isShort=False
        self.sellcondTime=0
        self.position=0
        self.gradCond=True
        self.gradCalVec=[]
        self.guardArr = GuardArr(50)
        self.openPrice=0
        self.stdVec=[]
        
    def setRSILevel(self, level):
        self.RSILevel = level
                
    def trade(self, price):
        #datetime_object = datetime.strptime(time, '%H:%M:%S')
        if self.isStart is True:
            #self.dateStart = datetime_object
            self.isStart=False
        else:
            #diff = datetime_object - self.dateStart
            
            
            #print (self.gainlossVec)
            #print (len(self.gainlossVec))
            if self.currTime > 14:
               averageGain = self.findAverageGain(self.first) 
               averageLoss = self.findAverageLoss(self.first)
               self.first = False
               self.gainlossVec= self.gainlossVec[1:]
               #self.gainlossVec.append(price)
               #print ('Avg Gain {0}, Avg Loss {1}'.format(averageGain, averageLoss))
               if averageLoss>0:
                   RS = averageGain/averageLoss
               else:
                   RS = 1000000
               self.RSI = 100 - 100 / (1+RS)
               if self.RSI < 31 :
                   #print ('Condition met')
                   self.buyCondition = True
                   #self.conditionTime = datetime_object 
                   self.condTime=self.currTime
                   #print ('Buy condition set to true')
               if self.RSI > 69:
                   self.sellCondition = True
                   self.sellcondTime=self.currTime
                   #print ('Sell condition set to true')
               #print ('RSI {0}'.format(self.RSI))
            if self.currTime==0:
                self.gainLossVec.append(0)
            else:
                self.gainlossVec.append(price-self.lastPrice)
                self.gradCalVec.append(price-self.lastPrice)
            
            if len(self.gradCalVec)>49:
                self.gradCalVec=self.gradCalVec[1:]
                self.checkGradCond()
            
        self.RSIVec.append(self.RSI)        
        self.lastPrice=price
        self.guardArr.insert(price)
        self.stdVec.append(self.guardArr.stdDev())
        #datetime_object = datetime.strptime(time, '%H:%M:%S')
        diff = self.currTime - self.condTime       
        if self.buyCondition is True and diff > 14:
            self.buyCondition is False
        diff = self.currTime - self.sellcondTime 
        if self.sellCondition is True and diff > 14:
            self.sellCondition is False
        self.currTime=self.currTime+1
        return True	
    def checkGradCond(self):
        totalGain=0
        totalLoss=0
        for i in range(0, len(self.gradCalVec)):
            if self.gradCalVec[i] < 0:
                totalLoss=totalLoss+abs(self.gradCalVec[i])
            else:
                totalGain= totalGain+self.gradCalVec[i]
        
        if (totalGain/totalLoss)>1.2:
            #print('set gradient to false')
            self.gradCond=False
        else:
            self.gradCond=True
            
    def findAverageGain(self, isFirst):
        if isFirst is True:
            for i in range(0,len(self.gainlossVec)-1):
                count=0
                sum=0.0
                #print ('length sum {0}'.format(len(self.gainlossVec)-1))
                #print ('sum {0}'.format(sum))
                if self.gainlossVec[i]>0.00:
                    count=count+1
                    sum=sum+self.gainlossVec[i]
            self.prevAvgGain = sum / 14
            return sum / 14.00
        else:
            currGain = self.gainlossVec[len(self.gainlossVec)-1]
            if currGain < 0:
                currGain = 0
            avgGain = (self.prevAvgGain * 13 + currGain) / 14
            self.prevAvgGain = avgGain
            return avgGain
            # if count > 0:
                # return sum / count
            # else:
                # return 0
                
    def findAverageLoss(self, isFirst):
        if isFirst is True:
            for i in range(0,len(self.gainlossVec)-1):
                count=0
                sum=0.0
                #print ('sum {0}'.format(sum))
                if self.gainlossVec[i]<0.00:
                    #print ('avg loss detected')
                    count=count+1
                    sum=sum+abs(self.gainlossVec[i])
            return sum / 14.00
                # if count > 0:
                    # return sum / count  
                # else:
                    # return 0
        else:
            currLoss = self.gainlossVec[len(self.gainlossVec)-1]
            if currLoss > 0:
                currLoss = 0
            else:
                currLoss = abs(currLoss)
            avgLoss = (self.prevAvgLoss * 13 + currLoss) / 14
            self.prevAvgLoss = avgLoss
            return avgLoss            
            
    def isBuy(self, price):
        #datetime_object = datetime.strptime(time, '%H:%M:%S')
        #diff = self.currTime-self.condTime
        if self.currTime > 15:
            if self.isOpen is False:
                        
                if (self.buyCondition is True) and (self.RSI > self.B_RSILevel) and (self.gradCond is True):
                    print('Buy Long cond: {0}, RSI: {1} '.format(self.buyCondition, self.RSI))
                    self.buyCondition  = False
                    self.bought = True
                    self.isOpen = True
                    self.isShort=False
                    self.position=1
                    self.openPrice = price
                    return True
                else:
                    #self.condition = False
                    #print ('Close Buy condition not met')
                    return False
            else:
                stdDev = self.guardArr.stdDev()
                stdPrice = self.openPrice +1.5* stdDev
                
                if (self.position == -1) and ((self.RSI< self.buyRSI) or (self.RSI > self.buyStopRSI) or (price > stdPrice)):
                    print ('Buy Close position: {0}'.format(self.position))
                    self.isOpen = False
                    self.sellCondition = False
                    self.bought = True
                    self.isShort=False
                    self.position=0
                    return True
                else:
                    #print ('Open Buy condition not met')
                    return False
            
    def isSell(self, price):
        #diff = self.currTime-self.condsellTime
        if self.currTime>15:
            if self.isOpen is True and self.position == 1:
                stdDev = self.guardArr.stdDev()
                stdPrice = self.openPrice -1.5* stdDev
                          
                if (self.RSI > self.sellRSI) or (self.RSI < self.stopRSI) or (price<stdPrice):
                    print('Sell Close')
                    #self.sellPrice=9999
                    self.buyCondition = False
                    #self.stopPrice=0
                    self.isOpen  = False
                    self.bought = False
                    self.position=0
                    return True
                else:
                    #print ('Open Sell condition not met')
                    return False
            else:
                if (self.sellCondition is True) and (self.RSI < self.S_RSILevel) and (self.gradCond is True):
                    print ('Sell Short')
                    self.sellCondition  = False
                    self.bought = False
                    self.isOpen = True
                    self.isShort=True
                    self.position=-1
                    self.openPrice = price
                    return True
                else:
                    #self.condition = False
                    #print ('Close sell condition not met')
                    return False 
            
            
    def getRSIVec(self):
        return self.RSIVec
    def getRSI(self):
        return self.RSI
    def getIsShort(self):
        return self.isShort
    def getIsOpen(self):
        return self.isOpen
        
    def getStdVec(self):
        return self.stdVec
        