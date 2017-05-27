
from Algorithm import Algorithm
from Display import Display
import matplotlib.pyplot as plt

class TradeBroker (object):
    def __init__(self, data, totalMoney, invest, algorithm, display):
        self.data = data
        self.totalMoney=totalMoney
        self.invest=invest
        self.algorithm=algorithm
        self.boughtLots=0
        self.Equity = totalMoney
        self.EquityVec = []
        self.trades = 0
        self.display = display
        
    def trade(self):
        annoVec = []
        for i in range (0, len(self.data)):
        #for i in range (0, 500):
            
            bidPrice = float(self.data[i]["Close"])
            time = self.data[i]["Time"]
            date = self.data[i]["Date"]
            self.algorithm.trade(date, time, bidPrice)
            anno = False
            if self.algorithm.isBuy(time, bidPrice) is True:
                print (i)
                print ('Buy price {0}'.format(bidPrice))
                self.boughtLots=self.invest/bidPrice
                self.totalMoney = self.totalMoney - self.invest
                self.trades = self.trades + 1
                annoVec.append('buy ' + str(bidPrice))
                anno = True
            if self.algorithm.isSell(bidPrice) is True:
                print (i)
                print ('Sell price {0}'.format(bidPrice))
                self.totalMoney = self.totalMoney + self.boughtLots*bidPrice
                self.boughtLots=0
                self.trades = self.trades + 1
                annoVec.append('sell '+ str(bidPrice))
                anno = True
            if anno is False:
                annoVec.append('')
            #print ('Total Money {0}'.format(self.totalMoney))
            self.Equity = self.totalMoney + self.boughtLots * bidPrice
            self.EquityVec.append(self.Equity)
        self.display.display(self.EquityVec, annoVec)
        #plt.plot(self.EquityVec)
        #ax = plt.subplots()
        #for i in range(0,len(self.data)):
        #    ax.annotate(annoVec[i], self.EquityVec[i])
        #plt.show()
        print ('Total Money {0} Trades {1}'.format(self.totalMoney, self.trades))

        
        