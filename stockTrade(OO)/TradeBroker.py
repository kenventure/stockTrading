
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
            bidPrice = float(self.data[i]["Close"])
            time = self.data[i]["Time"]
            date = self.data[i]["Date"]
            self.algorithm.trade(date, time, bidPrice)
			
            if self.algorithm.isBuy():
                self.boughtLots=self.invest/bidPrice
                self.totalMoney = self.totalMoney - self.invest
            if self.algorithm.isSell():
                self.totalMoney = self.totalMoney + self.boughtLots*bidPrice
                self.boughtLots=0