import pandas as pd
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
from time import time
import pickle 
from datetime import datetime
import requests
from binance.client import Client
from dateutil.relativedelta import relativedelta

api_key = 'HEREGOESYOUTAPIKEY'
api_secret = 'HEREGOESYOURAPISECRET'

def bitoda(data):

	"""
	This function transform data from binance into a dataframe
	:params: data: data to transform it should have the form  [openTime, open, high, low, close, volume, closeTime, quoteAssetVolume, numberOfTrades, Takerbuy...., takerbuy..., ignore]
	:return: Dataframe ith the columns  ['datetime', 'open', 'high', 'low', 'close', 'volume',] 
	"""
	
	# Create Dataframe
	historical = pd.DataFrame()
	dates = [datetime.utcfromtimestamp(sample[0]/1000) for sample in data]
	ope = [float(sample[1]) for sample in data]
	high = [float(sample[2]) for sample in data]
	low = [float(sample[3]) for sample in data]
	close = [float(sample[4]) for sample in data]
	volume = [float(sample[5]) for sample in data]
	
	historical['datetime'] = dates
	historical['open'] = ope
	historical['high'] = high
	historical['low'] = low
	historical['close'] = close
	historical['volume'] = volume

	return historical

def fetch_bitcoin_data(date=datetime.now()):
	"""
	Get all the historical data available in binance api from every minute
	:params: date:date wich get the data to
	:return: Pandas Dataframe with the columns ['datetime', 'open', 'high', 'low', 'close', 'volume',]
	"""

	global api_key
	global api_secret
	
	client = Client(api_key, api_secret)
	data = client.get_historical_klines('BTCEUR', Client.KLINE_INTERVAL_1MINUTE, '09/09/2009 00:00:00', date.strftime('%d/%m/%Y %H:%M:%S"'))  

	return bitoda(data)

def update_bitcoin_data(old_historical, date=datetime.now()):
	"""
	Update and older bitcoin data Dataframe
	:params: old_historical: old bitcoin data, date:date wich get the data to
	:return: Pandas Dataframe with new data appended
	"""
	
	global api_key
	global api_secret
		
	last_date = max(old_historical['datetime'])
	
	# data = [openTime, open, high, low, close, volume, closeTime, quoteAssetVolume, numberOfTrades, Takerbuy...., takerbuy..., ignore]
	client = Client(api_key, api_secret)
	data = client.get_historical_klines('BTCEUR', CLient.KLINE_INTERVAL_1MINUTE, last_date.strftime('%d/%m/%Y %H:%M:%S"') + relativedelta(minutes=1), date.strftime('%d/%m/%Y %H:%M:%S"'))  
	
	return pd.concat([old_historical, bitoda(data)])

def fetch_sentiment_data(data):
	"""
	NOT USED FOR THE MOMENT, THE SCRAPPER TAKES TOO MUCH TIME
	Get all the historical sentiment data from the dates of historical financial data
	:params: data: Pandas Dataframe with financial data
	:return: Pandas Dataframe with new sentiment analysis columns
	"""	
	r = requests.get(' https://api.senticrypt.com/v1/history/')
	r = [x.replace('signal', 'bitcoin') for x in r.json()]
	horas = []
	for x in r:
			horas = horas + [requests.get('http://api.senticrypt.com/v1/history/bitcoin-2020-02-13_20.json').json()]
	return horas 

def merge(sent_data, finan_data):
	"""
	NOT USED FOR THE MOMENT
	Merge the financial data and the sentimenta analysis data gathered from any of the other functions
	:params: sent_data: pandas datafram with sentiment analysis data, finan_data: pandas dataframe with financial data
	:return: data: pandas dataframe ready to be splitted and used in train
	"""
	pass

def toten(data):
	"""
	Filter the minute to minute bitcoin data in order to get 10 minutes data
	:params: data: Pandas Dataframe qith financial data
	:return: Data dataframe in minutes
	"""
	return data[data['datetime'].minutes%10 == 0]

def window_data(n=10):
	"""
	Prepares the data in windows of size 10 and splits it in train, test
	:params: n:window size
	:return: x_train, y_train, x_test, y_test
	"""
	data = TimeseriesGenerator(train_x, train_y, length=10, batch_size=len(bit))
	X = np.array([MinMaxScaler().fit_transform(x) for x in data[0][0]])
	# X = np.array([x for x in data[0][0]])
	Y = data[0][1]
	x_train = X[:int(len(X)*0.75)]
	y_train = Y[:int(len(Y)*0.75)]
	x_test  = X[int(len(X)*0.75):]
	y_test  = Y[int(len(X)*0.75):]

	return x_train, y_train, x_test, y_test

def get_last(n=10, date=datetime.now()):
	"""
	Gets the last n sized window from now in order to predict it on the rnn
	:params: n:window size
	:return: x: data ready to feed the rnn
	"""
	global api_key
	global api_secret
	dates = []	
	client = Client(api_key, api_secret)
	for _ in range(10):
		dates + [date]	
		date = date - relativedelta(minutes=10)	
	data = client.get_historical_klines('BTCEUR', Client.KLINE_INTERVAL_1MINUTE,(date - relativedelta(minutes=110)).strftime('%d/%m/%Y %H:%M:%S'), date.strftime('%d/%m/%Y %H:%M:%S'))  
	data = bitoda(data)
	data = data[data['datetime'].isin(dates)]

	return data
	

if __name__ == '__main__':
	t1 = time()
	data = fetch_bitcoin_data()
	data = toten(data)
	t2 = t1 - time()
	print(data)
	print(t2)
