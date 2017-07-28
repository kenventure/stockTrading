import datetime
from TimeCheck import TimeCheck

class OpenCloseCheck (TimeCheck):
    def __init__(self, openTime, closeTime, clearTime):
         self.openTime=openTime
         self.closeTime=closeTime
         self.clearTime=clearTime
         
    def isOpen(self):
        currTime=datetime.datetime.now()
        #print(currTime)
        #print(self.openTime)
        #print(self.closeTime)
        #print(datetime.datetime.now().weekday())
        if datetime.datetime.now().weekday() <5 and currTime.time()>self.openTime and currTime.time()<self.closeTime:
            return True
        else:
            return False
            
    def isClear(self):
        #print( self.clearTime)
        compTime = (datetime.datetime.combine(datetime.date.today(), self.clearTime) + datetime.timedelta(seconds=60)).time()
        #print(compTime)
        if datetime.datetime.now().weekday() < 5 and datetime.datetime.now().time() > self.clearTime and (datetime.datetime.now().time()<compTime):
            return True
        else:
            return False