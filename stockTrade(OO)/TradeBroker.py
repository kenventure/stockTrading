
from Algorithm import Algorithm

class TradeBroker (object):
    def __init__(self, data, totalMoney, invest, algorithm):
        self.data = data
        self.totalMoney=totalMoney
        self.invest=invest
        self.algorithm=algorithm
        self.boughtLots=0
		
    def trade(self):
        for i in range (0, len(self.data)):
        #for i in range (0, 500):
            print (i)
            bidPrice = float(self.data[i]["Close"])
            time = self.data[i]["Time"]
            date = self.data[i]["Date"]
            self.algorithm.trade(date, time, bidPrice)
			
            if self.algorithm.isBuy(time, bidPrice) is True:
                print ('Buy')
                self.boughtLots=self.invest/bidPrice
                self.totalMoney = self.totalMoney - self.invest
            if self.algorithm.isSell(bidPrice) is True:
                print ('Sell')
                self.totalMoney = self.totalMoney + self.boughtLots*bidPrice
                self.boughtLots=0
            print ('Total Money {0}'.format(self.totalMoney))
                
        print ('Total Money {0}'.format(self.totalMoney))

        
        