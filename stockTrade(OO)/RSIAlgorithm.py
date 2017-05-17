from Algorithm import Algorithm
from datetime import datetime

class RSIAlgorithm(Algorithm):
    def __init__(self, intervalMin):
        self.intervalMin = intervalMin
        self.isStart=True
        self.lastPrice=0
        self.gainlossVec=[]

        
    def trade(self, date, time, price):
        datetime_object = datetime.strptime(date, '%m/%d/%Y')
        if self.isStart is True:
            self.dateStart = datetime_object
            self.isStart=False
        else:
            diff = datetime_object - self.dateStart
            
            self.gainlossVec.append(price-self.lastPrice)
            
            
            if diff.minutes > 14*5:
                
                
                
        self.lastPrice=price
        return True		

    def isBuy(self):
        return True

    def isSell(self):
        return True
        