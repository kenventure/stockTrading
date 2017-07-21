
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
from stockLight import LSClient,Subscription
from threading import Lock
import copy

    
class IGTradeBrokerNDMulti (object):
    def __init__(self, totalMoney, invest, algorithm):
        #self.data = data
        self.totalMoney=totalMoney
        self.invest=invest
        self.algorithm=algorithm
        self.boughtLots=0
        self.Equity = totalMoney
        #self.EquityVec = []
        self.trades = 0
        #self.display = display
        self.currPrice=0
        self.currPriceList={}
        self.algoList={}
        self.list1=[]
        self.list1.append("IX.D.DOW.IFG.IP")
        self.list1.append("IX.D.HANGSENG.IFG.IP")
        self.list1.append("IX.D.DAX.IFG.IP")
        for name in self.list1:
            temp = copy.deepcopy(algorithm)
            self.algoList[name]=temp
           
        self.delay = 60
 
        self.mutex = Lock()
        self.login()
        self.currPriceList={}
        
        
        




    def on_item_update(self, item_update):
        #print('item update')
        #print("Bid {0}".format(**item_update["BID"]))
        #print("{stock_name:<19}: Last{last_price:>6} - Time {time:<8} - "
        #      "Bid {bid:>5} - Ask {ask:>5}".format(**item_update["values"]))
        #print(item_update)
        print("Bid {BID:>5} - Ask {OFFER:>5} - Update Time {UPDATE_TIME:<20} Name".format(**item_update["values"]))
        print((item_update["name"])[7:])
        
        strPrice="{BID:>5}".format(**item_update["values"])
        #print(strPrice)
        self.mutex.acquire()
        name=item_update["name"][7:]
        self.currPriceList[name]=float(strPrice)
        self.currPrice=float(strPrice)
        self.mutex.release()
        print(self.currPriceList)
     
    def connectLightStreamer(self, password):
        self.lightstreamer_client = LSClient("https://demo-apd.marketdatasystems.com", "DEFAULT", user="lthams", password=password)
        try:
            self.lightstreamer_client.connect()
        except Exception as e:
            print("Unable to connect to Lightstreamer Server")
            print(traceback.format_exc())
            sys.exit(1)
        itemsList=[]
        for item in self.list1:
            name="MARKET:"+item
            itemsList.append(name)
            self.currPriceList[name[7:]]=0
        print(self.currPriceList)
        self.subscription = Subscription(
        mode="MERGE",
        items=itemsList,
        fields=["BID", "OFFER", "UPDATE_TIME"])
        self.subscription.addlistener(self.on_item_update)
        sub_key = self.lightstreamer_client.subscribe(self.subscription)
    
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
        self.passwordCAT = "CST-"+r.headers['CST']+"|"+"XST-"+r.headers['X-SECURITY-TOKEN']
        self.connectLightStreamer(self.passwordCAT)
        print('finish')
        
    def getTradePrice(self):
        return self.currPrice

    def placePosition(self, isBuy, stock):
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
        "epic": stock,
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
        #annoVec = []
        #priceVec=[]
        #lastPrice=0
        entryPrice=0
        totalAtEntry=0
        while True:
        #for i in range (0, 1000):   
            
            
            print('trade')
            for stock in self.list1:
                self.mutex.acquire()
                #bidPrice = self.getTradePrice()
                bidPrice=self.currPriceList.get(stock)
                self.mutex.release()
                if bidPrice is None or bidPrice == 0:
                    print('Bid price wrong {0} Curr price {1}'.format(bidPrice, self.currPrice))
                    time.sleep(self.delay)
                    continue
                print ("Resolving...")
                myAlgo = self.algoList.get(stock)
                myAlgo.trade(bidPrice)
                anno = False
                self.boughtLots=50
                
                RSI = myAlgo.getRSI()
                print ("RSI {0}".format(RSI))
                if myAlgo.isBuy(bidPrice) is True:
                    #print (i)
                    print ('Buy price {0} RSI {1}'.format(bidPrice, RSI))
                    #self.boughtLots=self.invest/bidPrice
                    totalAtEntry=self.totalMoney
                    self.totalMoney = self.totalMoney - self.boughtLots*bidPrice
                    self.trades = self.trades + 1
                    #annoVec.append('buy ' + str(bidPrice))
                    self.placePosition(True, stock)
                    #annoVec.append('b')
                    anno = True
                    entryPrice=bidPrice
                    print('')
                if myAlgo.isSell(bidPrice) is True:
                    #print (i)
                    print ('Sell price {0} RSI{1}'.format(bidPrice, RSI))
                    totalAtEntry=self.totalMoney
                    self.totalMoney = self.totalMoney + self.boughtLots*bidPrice
                    #self.boughtLots=0
                    self.trades = self.trades + 1
                    #annoVec.append('sell '+ str(bidPrice))
                    #annoVec.append('s')
                    anno = True
                    entryPrice=bidPrice
                    self.placePosition(False, stock)
                    print('')
                #if anno is False:
                #    annoVec.append('')
                #print ('Total Money {0}'.format(self.totalMoney))
                #self.Equity = self.totalMoney + self.boughtLots * bidPrice
                #isShort = myAlgo.getIsShort()
                #gain = bidPrice-entryPrice
                #isOpen = myAlgo.getIsOpen()
                
                #if isOpen is True:
                #   if isShort is True:
                #        self.Equity = totalAtEntry - gain * self.boughtLots 
                #    else:
                #        self.Equity = totalAtEntry + gain * self.boughtLots 
                #else:
                #    self.Equity = self.totalMoney
                #self.EquityVec.append(self.Equity)
                #priceVec.append(bidPrice)
                print('Total trades {0} Time: {1}'.format(self.trades, datetime.datetime.utcnow()))
                #lastPrice=bidPrice
            time.sleep(self.delay)
            
        #self.display.display(self.EquityVec, annoVec, priceVec, self.algorithm.getRSIVec(), self.algorithm.getStdVec())
        #self.display.log(self.EquityVec, annoVec, priceVec)
        #plt.plot(self.EquityVec)
        #ax = plt.subplots()
        #for i in range(0,len(self.data)):
        #    ax.annotate(annoVec[i], self.EquityVec[i])
        #plt.show()
        print ('Total Money {0} Trades {1}'.format(self.totalMoney, self.trades))
    
        
        