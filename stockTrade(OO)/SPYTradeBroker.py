
from Algorithm import Algorithm
from Display import Display
import matplotlib.pyplot as plt

class SPYTradeBroker (object):
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
        priceVec=[]
        lastPrice=0
        entryPrice=0
        totalAtEntry=0
        #for i in range (0, len(self.data)):
        for i in range (0, 1000):
            
            bidPrice = float(self.data[i]["Close"])
            time = self.data[i]["Time"]
            date = self.data[i]["Date"]
            self.algorithm.trade(bidPrice)
            anno = False
            self.boughtLots=1000
            RSI = self.algorithm.getRSI()
            if self.algorithm.isBuy(bidPrice) is True:
                print (i)
                print ('Buy price {0} RSI {1}'.format(bidPrice, RSI))
                #self.boughtLots=self.invest/bidPrice
                totalAtEntry=self.totalMoney
                self.totalMoney = self.totalMoney - self.boughtLots*bidPrice
                self.trades = self.trades + 1
                #annoVec.append('buy ' + str(bidPrice))
                annoVec.append('b')
                anno = True
                entryPrice=bidPrice
                print('')
            if self.algorithm.isSell(bidPrice) is True:
                print (i)
                print ('Sell price {0} RSI{1}'.format(bidPrice, RSI))
                totalAtEntry=self.totalMoney
                self.totalMoney = self.totalMoney + self.boughtLots*bidPrice
                #self.boughtLots=0
                self.trades = self.trades + 1
                #annoVec.append('sell '+ str(bidPrice))
                annoVec.append('s')
                anno = True
                entryPrice=bidPrice
                print('')
            if anno is False:
                annoVec.append('')
            #print ('Total Money {0}'.format(self.totalMoney))
            #self.Equity = self.totalMoney + self.boughtLots * bidPrice
            isShort = self.algorithm.getIsShort()
            gain = bidPrice-entryPrice
            isOpen = self.algorithm.getIsOpen()
            
            if isOpen is True:
                if isShort is True:
                    self.Equity = totalAtEntry - gain * self.boughtLots 
                else:
                    self.Equity = totalAtEntry + gain * self.boughtLots 
            else:
                self.Equity = self.totalMoney
            self.EquityVec.append(self.Equity)
            priceVec.append(bidPrice)
            
            lastPrice=bidPrice
            
        self.display.display(self.EquityVec, annoVec, priceVec, self.algorithm.getRSIVec())
        self.display.log(self.EquityVec, annoVec, priceVec)
        #plt.plot(self.EquityVec)
        #ax = plt.subplots()
        #for i in range(0,len(self.data)):
        #    ax.annotate(annoVec[i], self.EquityVec[i])
        #plt.show()
        print ('Total Money {0} Trades {1}'.format(self.totalMoney, self.trades))

        
        