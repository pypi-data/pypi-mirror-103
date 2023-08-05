# Import Modules & Functions
import pandas as pd
from pandas import DataFrame
from pandas import read_csv, read_excel
from pandas import Series
from numpy import log
from statistics import stdev
from datetime import date, timedelta, datetime
from time import sleep
import time
import requests
import ast
from multiprocessing import Pool
import threading
from threading import Timer, Event, Thread
import json


#Importing Modules, setting starting parameters and defining classes

# The class to create an object for every isin and to keep the live information of it.
class Isin:
    def __init__(self, name):
        # isin's name
        self.name= name
        # This is the Persian symbol of the isin.
        self.persian_id= ''
        #The bourse id to crawl from the tsetmc
        self.bourse_id= ''
        
        #This part sets the initial parameters. They will be adjusted if the isin is in the continous run.
        # This fixes the activation status of the isin.
        self.activate= True
        # The free budget of the isin: 
        self.budget= 0
        # This is servers's time Ud
        self.server_time= None
        # The lastTrade Time Ud
        self.lastTrade_Time= None
        self.Old_lastTrade = None
        # This shows the state of the Stockwatch data. Ud
        self.state= None
        # This represents the last Mean Reversion Test result. Ud
        self.MR_Test= False
        # This is the half life of mean reversion if MR_Test is True and 0 if not. Ud
        self.half_life_number= 0
        # This event is normally None, Buy in Buy-position and Sell in Sell-position.
        self.event= None
        # This is False when we don't hold any share of the isin and True if we hold a share.
        self.Hold= False
        # This shows the volume of the share of the isin we hold at the moment.
        self.HoldVolume= 0
        # This is the last price recorded in the market. Ud
        self.Last_Price= 0
        # This is to check if the commision condition is accuired according to standard deviation and expected return. UD
        self.Commission_Cond= False
        # This shows the instantanous Mouving Average Ud
        self.SMA= 0
        # This calculates the Buy Limit for Enter function according to SMA and st_dev. Ud
        self.Buy_Limit= 0
        # This is Benefit limit to sell the shares of the isin. Ud
        self.Ben_Limit= 0
        # This is Loss Limit to sell the shares of the isin. Ud
        self.Loss_Limit= 0
        # This is the standard deviation of the last price records.  Ud
        self.st_dev= 0 

def Create_isin_object(isn):
    return Isin(isn)


#The Class to repeat a function as threading module every n seconds
class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()

def Repeat_Function(interval, function, *args, **kwargs):
    RepeatedTimer(interval, function, *args, **kwargs)
    
# What about stopping a function?

# Getting StockWatch data

def TSE_Close_Daily(bourse_id):
    url_daily_data_tsetmc= 'http://tsetmc.com/tsev2/data/Export-txt.aspx?t=i&a=1&b=0&i=???'
    url_daily_data= url_daily_data_tsetmc.replace('i=???', 'i='+ bourse_id)
    daily_data= requests.get(url_daily_data)
    daily_data= read_csv(io.StringIO(daily_data.text))
    daily_data= pd.DataFrame(daily_data)
    daily_data= daily_data['<CLOSE>'].values
    #daily_data= daily_data[::_frequency]
    daily_data= daily_data[::-1]
    return daily_data
    #daily_data= pd.DataFrame(daily_data, columns= ['Close'])
    #return daily_data

def dataengine_Data(isn, number_of_records, _frequency):
    _number_of_records= 10 * number_of_records * _frequency
    'https://omid.algo.ir/api/dataengine/candle/minutely?isin=IRO1TMLT0001&page=0&size=100&from=2020-06-24&to=2020-07-08'
    url_SW_dataengine = 'https://omid.algo.ir/api/dataengine/candle/_period?isin=??&page=0&size=???&from=???&to=???'
    # Fixing of the parameters of the request to dataengine api
    DAYS= _number_of_records//180 +5
    Beginning_Date= datetime.today() + timedelta(days=-DAYS)
    Beginning_Date= Beginning_Date.strftime('%Y-%m-%d')
    Tomorrow_Date= datetime.today() + timedelta(days=1)
    Tomorrow_Date= Tomorrow_Date.strftime('%Y-%m-%d')
    url_SW_dataengine= url_SW_dataengine.replace('_period', 'minutely')
    url_SW_dataengine= url_SW_dataengine.replace('isin=??', 'isin='+ isn)
    url_SW_dataengine= url_SW_dataengine.replace('size=???', 'size=' + str(_number_of_records))
    url_SW_dataengine= url_SW_dataengine.replace('from=???', 'from='+ Beginning_Date)
    url_SW_dataengine= url_SW_dataengine.replace('to=???', 'to='+ Tomorrow_Date)
    # sending the request and processing the response
    for i in range(1,100):
        try:
            data_SW_dataengine = requests.get(url = url_SW_dataengine)
            break
        except OSError:
            sleep(1)
    data_SW_dataengine = data_SW_dataengine.json()['content']
    data_SW_dataengine = pd.DataFrame.from_dict(data_SW_dataengine)
    try:
        data_SW_dataengine= data_SW_dataengine['closePrice']
    except:
        return
    data_SW_dataengine= data_SW_dataengine[::_frequency]
    data_SW_dataengine= data_SW_dataengine[len(data_SW_dataengine) - number_of_records: ]
    # changing the close price to a list, applying _frequency, getting the last records, and changing to a DataFrame.
    data_SW_dataengine= data_SW_dataengine.values
    
    #data_SW_dataengine= pd.DataFrame(data_SW_dataengine, columns= ['last'])
    return data_SW_dataengine
    
# This function gets the Stockwatch data from omid core api and returns it as a one row Data Frame
def Get_SW_Data(isn, Maximum_Permitted_Delay):
    url_SW= 'https://omid.algo.ir/api/core/stockwatch/isn=??'
    TimeFormat= '%Y-%m-%d %H:%M:%S'
    url_SW_UD= url_SW
    url_SW_UD= url_SW_UD.replace('isn=??', isn)
    for i in range (1,Maximum_Permitted_Delay):
        try:
            Data_SW_UD = requests.get(url = url_SW_UD)
        except OSError:
            sleep(1)
            if i== Maximum_Permitted_Delay - 1:
                return None
    Data_SW= Data_SW_UD.content.decode("utf-8")
    try:
        Data_SW= ast.literal_eval(Data_SW)
    except:
        return None
    Data_SW= pd.DataFrame([Data_SW])
    dateTime= pd.to_datetime(Data_SW.loc[0,'dateTime'])
    lastTrade= pd.to_datetime(Data_SW.loc[0,'lastTrade'])
    currentTime= pd.to_datetime(datetime.now().strftime(TimeFormat))
    dateTimeDelay= (currentTime - dateTime).total_seconds()
    lastTradeDelay= (currentTime - lastTrade).total_seconds()
    if (dateTimeDelay > Maximum_Permitted_Delay):
        return 'Delay in data'
    elif (lastTradeDelay > Maximum_Permitted_Delay):
        return None
    return Data_SW

# This function gets the BidAsk data from omid.algo.ir/api/core  and returns it as a five row Data Frame and returns None in case of exception or delay in case of dalay in information. 

def Get_BidAsk_Data(isn, Maximum_Permitted_Delay):
    url_BidAsk= 'https://omid.algo.ir/api/core/bidask/isn=??'
    TimeFormat= '%Y-%m-%d %H:%M:%S'
    url_BidAsk_UD= url_BidAsk
    url_BidAsk_UD= url_BidAsk_UD.replace('isn=??', isn)
    for i in range (1,60):
        try:
            Data_BidAsk_UD = requests.get(url = url_BidAsk_UD)
        except OSError:
            sleep(1)
    Data_BidAsk= Data_BidAsk_UD.content.decode("utf-8")
    try:
        Data_BidAsk= ast.literal_eval(Data_BidAsk)
    except:
        return None
    BidAsk_dateTime= pd.to_datetime(Data_BidAsk["dateTime"])  
    Data_BidAsk= Data_BidAsk["items"]
    Data_BidAsk= pd.DataFrame(Data_BidAsk)
    currentTime= pd.to_datetime(datetime.now().strftime(TimeFormat))
    dateTimeDelay= (currentTime - BidAsk_dateTime).total_seconds()
    if (dateTimeDelay > Maximum_Permitted_Delay):
        return 'Delay in BidAsk data'
    return Data_BidAsk

def is_SW_online(isn, Maximum_Permitted_Delay):
    TimeFormat= '%Y-%m-%d %H:%M:%S'
    currentTime= pd.to_datetime(datetime.now().strftime(TimeFormat))
    New_Data= Get_SW_Data(isn, Maximum_Permitted_Delay)
    # This is server's time
    server_time= New_Data.loc[0,'dateTime']
    if (currentTime - pd.to_datetime(server_time)).total_seconds() > Maximum_Permitted_Delay:
        return False
    else:
        return True
    
def is_trade_time():
    TimeFormat= '%Y-%m-%d %H:%M:%S'
    # Begin & End Time of the Market
    Begin_Time= '09:00:00'
    End_Time= '12:30:00'
    currentTime= pd.to_datetime(datetime.now().strftime(TimeFormat))
    BeginTime= pd.to_datetime(Begin_Time)
    EndTime= pd.to_datetime(End_Time)
    if  (currentTime - BeginTime).total_seconds() < 0 or (EndTime - currentTime).total_seconds() < 0 :
        return False
    else:
        return True
    
def Send_Order(account_user, account_password, user_Id, isn, Price, Volume, side):
    return
    #account_user= "azadifaraz"
    #account_password= "123456$aA"
    #user_Id= "bfdacd8a-0ae7-4897-8f2f-0300d94025eb"
    url_token = "https://omid.algo.ir/api/omid/user/login-without-captcha"
    url_order = "https://omid.algo.ir/api/omid/order"
    _account_user= "\"" + account_user + "\""
    _account_password= "\"" + account_password + "\""
    _user_Id= "\"" + user_Id + "\""
    _side= "\"" + side + "\""
    
    payload="{\n    \"userName\":"+ _account_user + ",\n    \"password\":"+ _account_password + ",\n    \"token\":\"\",\n    \"captcha\":\"\"\n}" 
    headers = {  'Content-Type': 'application/json'}
    response = requests.request("POST", url_token, headers=headers, data=payload)
    print(response.json())
    token= response.json()['token']
    
    price= Price
    quantity= Volume
    _isn= "\""+ isn + "\""
    payload="{\n    \"isin\":" +_isn + ",\n    \"userId\":"+  _user_Id + ",\n    \"price\":"+ str(price) + ",\n    \"quantity\": "+ str(quantity) +",\n    \"validity\": \"FILL_AND_KILL\",\n    \"side\":" + _side + "\n}"
    headers = {  'Token': token,  'Content-Type': 'application/json'}
    response = requests.request("POST", url_order, headers=headers, data=payload)
    message= response.json()["message"]
    print(message)
    print ('OK!')
    return     
    