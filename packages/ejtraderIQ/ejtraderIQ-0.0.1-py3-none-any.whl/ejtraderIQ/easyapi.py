from .stable_api import IQ_Option
import logging
import time
import os


class IQOption:
    __version__ = "7.8.9.1"


    def __init__(self, email, password, account_type, verbose = False, checkConnection = False):
        self.email = email
        self.password = password
        self.account_type = account_type
        self.debug = verbose
        self.iq = None
        self.checkConnection = checkConnection


        if self.debug:
            logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

        if self.iq == None:
            self.connect()
            


    def connect(self):
        print("Trying to connect to IqOption")
        self.iq = IQ_Option(self.email,self.password)
        self.iq.connect()


        if self.iq != None:
            while True:
                if self.iq.check_connect() == False:

                    print('Error when trying to connect')
                    print(self.iq)
                    print("Retrying")
                    self.iq.connect()
                else:
                    if not self.checkConnection:
                        print('Successfully Connected! Account type : ' + self.account_type)
                    break
                    time.sleep(3)
                if self.account_type == "DEMO":
                    self.iq.change_balance("PRACTICE") # PRACTICE or REAL
                    
                elif self.account_type == "REAL":
                    self.iq.change_balance("REAL") # PRACTICE or REAL


    # Private Functions
    def __timeframe_to_sec(self,timeframe):
        # Timeframe dictionary
        TIMECANDLE = {
            "S30": 30,
            "M1": 60,
            "M2": 120,
            "M3": 180,
            "M4": 240,
            "M5": 300,
            "M15": 900,
            "M30": 1800,
            "H1": 3600,
                
        }
        return TIMECANDLE[timeframe]             
    def __timeframe_to_trading(self,timeframe):
        # Timeframe dictionary
        TIMETTRADE = {
            "S30": 1,
            "M1": 1,
            "M2": 2,
            "M3": 3,
            "M4": 4,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 60,
                
        }
        return TIMETTRADE[timeframe]

    def buy(self, contract, symbol, timeframe):
        timeframe = self.__timeframe_to_trading(timeframe)
        done, id = self.iq.buy(contract, symbol, "call", int(timeframe))
        
        if not done:
            print('Error call')
            print(done, id)
            exit(0)
        
        return id

    def sell(self, contract, symbol, timeframe):
        timeframe = self.__timeframe_to_trading(timeframe)
        done, id = self.iq.buy(contract, symbol, "put", int(timeframe))
        
        if not done:
            print('Error put')
            print(done, id)
            exit(0)
        
        return id   
    
    def balance(self):
        return self.iq.get_balance()

    def isOpen(self):
        isOpen = []
        opened_market=self.iq.get_all_open_time()
        
        for type_name, data in opened_market.items():
            for Asset,value in data.items():
                if value['open'] == True:
                    value = 'open'
                else:
                    value = 'close'
                result = {
                "Asset": Asset,
                "Type" : type_name, 
                "Status" : value
                }
                isOpen.append(result)
            
        return isOpen

    def payout(self, symbol, style=None):
        if not style:
            style = 'turbo'
        payout = self.iq.get_all_profit()   
        return payout[symbol][style]

    def remaning(self, timeframe):
        t = self.__timeframe_to_trading(timeframe)
        remaning_time=self.iq.get_remaning(t)
        purchase_time=remaning_time
        return purchase_time

    def checkwin(self,id):
         return self.iq.check_win_v3(id)


    def powerbar_live(self, symbol):
        return self.iq.start_mood_stream(symbol)

    def powerbar_history(self, symbol):
        return self.iq.get_traders_mood(symbol)