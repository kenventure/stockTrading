
from Algorithm import Algorithm
from Display import Display
#import matplotlib.pyplot as plt
import requests
import base64
import json 
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 
import time
import datetime

class IGTradeBrokerND (object):
    def __init__(self, totalMoney, invest, algorithm):
        #self.data = data
        self.totalMoney=totalMoney
        self.invest=invest
        self.algorithm=algorithm
        self.boughtLots=0
        self.Equity = totalMoney
        self.EquityVec = []
        self.trades = 0
        #self.display = display
        self.login()
        self.delay = 60
        
    def login(self):
        url = "https://demo-api.ig.com/gateway/deal"
        identifier = "lthams"
        password = "1q2w3e4rT"
        m_apiKey = "2816010fc8a0d7c446393955d5b3e922c1b1b955"
        session = "/session/encryptionKey"
        m_url = url + session
        headers = { "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "X-IG-API-KEY": m_apiKey
        } 
        # In[]
        r = requests.get(m_url, headers=headers)
        # In[] 
        m_data = r.json() 
        decoded = base64.b64decode(m_data['encryptionKey'])
        rsakey = RSA.importKey(decoded)
        message = password + '|' + str(int(m_data['timeStamp']))
        input = base64.b64encode(message.encode())
        encryptedPassword = base64.b64encode(PKCS1_v1_5.new(rsakey).encrypt(input))
        session = "/session"
        m_url = url + session
        headers = { "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "X-IG-API-KEY": m_apiKey,
        "Version": "2"
        } 
        payload = json.dumps({ "identifier": identifier,
        "password": encryptedPassword.decode('utf-8'),
        "encryptedPassword": True
        }) 
        # In[]
        r = requests.post(m_url, data=payload, headers=headers)
        r.status_code
        print (r.status_code)
        print (r.text)
        print (r.headers)
        self.apiKey = m_apiKey
        self.token = r.headers['X-SECURITY-TOKEN']
        self.CST = r.headers['CST']
        
    def getTradePrice(self):
        #urlMarket = "https://demo-api.ig.com/gateway/deal/prices/IX.D.DOW.IFG.IP"
        urlMarket = "https://demo-api.ig.com/gateway/deal/prices/IX.D.DOW.IFG.IP/MINUTE/3"
        headers = { "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "X-IG-API-KEY": self.apiKey,
        "Version": "2",
        "X-SECURITY-TOKEN": self.token,
        "CST": self.CST
        }

        r1 = requests.get(urlMarket, headers = headers)

        print(r1.status_code)
        #print (r1.text) 
        if r1.status_code == 200:
            json_data = json.loads(r1.text)

            prices = json_data["prices"]

            #print prices

            lastLot = prices[len(prices)-1]
            
            closePrice = lastLot['closePrice']['bid']

            print closePrice
            if closePrice is None or closePrice == "":
                return 0
            else:
                return float(closePrice)                
        else:
            print (r1.headers)
            print (r1.text)
            #self.login()
            return 0

    def placePosition(self, isBuy):
        urlPosition="https://demo-api.ig.com/gateway/deal/positions/otc"


        headers = { "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "X-IG-API-KEY": self.apiKey,
        "Version": "2",
        "X-SECURITY-TOKEN": self.token,
        "CST": self.CST
        }

        if isBuy is True:
            position = "BUY"
            
        else:
            position = "SELL"
            
        data = {
        "currencyCode":"SGD",
        "direction":position,
        "epic": "IX.D.DOW.IFG.IP",
        "expiry": "-",
        "forceOpen":"false",
        "guaranteedStop":"false",
        "level":None,
        "limitDistance":None,
        "limitLevel":None,
        "orderType":"MARKET",
        "quoteId":None,
        "size": "1",
        "stopDistance":None,
        "stopLevel":None,
        "timeInForce":"EXECUTE_AND_ELIMINATE",
        "trailingStop":"false",
        "trailingStopIncrement":None
        }

        payload=json.dumps(data)

        r1 = requests.post(urlPosition, data=payload, headers = headers)

        print(r1.status_code)
        print (r1.headers)
        print (r1.text) 
        
    def trade(self):
        annoVec = []
        priceVec=[]
        lastPrice=0
        entryPrice=0
        totalAtEntry=0
        while True:
        #for i in range (0, 1000):   
            bidPrice = self.getTradePrice()
            if bidPrice is None or bidPrice == 0:
                time.sleep(self.delay)
                continue
                print ("Resolving...")
            self.algorithm.trade(bidPrice)
            anno = False
            self.boughtLots=50
            RSI = self.algorithm.getRSI()
            print ("RSI {0}".format(RSI))
            if self.algorithm.isBuy(bidPrice) is True:
                #print (i)
                print ('Buy price {0} RSI {1}'.format(bidPrice, RSI))
                #self.boughtLots=self.invest/bidPrice
                totalAtEntry=self.totalMoney
                self.totalMoney = self.totalMoney - self.boughtLots*bidPrice
                self.trades = self.trades + 1
                #annoVec.append('buy ' + str(bidPrice))
                self.placePosition(True)
                annoVec.append('b')
                anno = True
                entryPrice=bidPrice
                print('')
            if self.algorithm.isSell(bidPrice) is True:
                #print (i)
                print ('Sell price {0} RSI{1}'.format(bidPrice, RSI))
                totalAtEntry=self.totalMoney
                self.totalMoney = self.totalMoney + self.boughtLots*bidPrice
                #self.boughtLots=0
                self.trades = self.trades + 1
                #annoVec.append('sell '+ str(bidPrice))
                annoVec.append('s')
                anno = True
                entryPrice=bidPrice
                self.placePosition(False)
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
            print('Total trades {0} Time: {1}'.format(self.trades, datetime.datetime.utcnow()))
            lastPrice=bidPrice
            time.sleep(self.delay)
            
        #self.display.display(self.EquityVec, annoVec, priceVec, self.algorithm.getRSIVec(), self.algorithm.getStdVec())
        #self.display.log(self.EquityVec, annoVec, priceVec)
        #plt.plot(self.EquityVec)
        #ax = plt.subplots()
        #for i in range(0,len(self.data)):
        #    ax.annotate(annoVec[i], self.EquityVec[i])
        #plt.show()
        print ('Total Money {0} Trades {1}'.format(self.totalMoney, self.trades))
    
        
        