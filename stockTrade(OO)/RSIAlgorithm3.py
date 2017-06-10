from Algorithm import Algorithm
from datetime import datetime

class RSIAlgorithm3(Algorithm):
    def __init__(self, intervalMin):
        self.intervalMin = intervalMin
        self.isStart=True
        self.lastPrice=0
        self.gainlossVec=[]
        self.condition = False
        #self.conditionTime=datetime(2010, 9, 12, 11, 19, 54)
        self.sellPrice=0.0
        self.stopPrice = 0.0
        self.first = True
        self.prevAvgLoss = 0.0
        self.bought = False
        self.RSI=0
        self.RSIVec=[]
        self.RSILevel = 40
        self.sellRSI=69
        self.stopRSI=29
        self.condTime=0
        self.currTime=0
    def setRSILevel(self, level):
        self.RSILevel = level
                
    def trade(self, price):
        #datetime_object = datetime.strptime(time, '%H:%M:%S')
        if self.isStart is True:
            #self.dateStart = datetime_object
            self.isStart=False
        else:
            #diff = datetime_object - self.dateStart
            
            self.gainlossVec.append(price-self.lastPrice)
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
               if self.RSI < 31:
                   #print ('Condition met')
                   self.condition = True
                   #self.conditionTime = datetime_object 
                   self.condTime=self.currTime
               #print ('RSI {0}'.format(self.RSI))
        self.RSIVec.append(self.RSI)        
        self.lastPrice=price
        
        #datetime_object = datetime.strptime(time, '%H:%M:%S')
        diff = self.currTime - self.condTime       
        if self.condition is True and self.currTime > 14:
            self.condition is False
        self.currTime=self.currTime+1
        return True		
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
        diff = self.currTime-self.condTime
        if self.condition is True and self.RSI > self.RSILevel and diff < 15 and self.bought is False:

            #self.condition  = False
            self.bought = True
            return True
        else:
            #self.condition = False
            return False

    def isSell(self, price):
        if (self.RSI > self.sellRSI or self.RSI < self.stopRSI) and self.bought is True:
            #self.sellPrice=9999
            self.condition=False
            #self.stopPrice=0
            self.bought  = False
            return True
        else:
            return False
            
    def getRSIVec(self):
        return self.RSIVec
        