import fetch_data as feda
import pandas as pd
import numpy as np
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler

def prepare_data(train_size=0.80):
		
                bit = pd.read_csv('bitcoin_data', sep=';')
            
		train_x = bit[['open', 'high', 'low', 'close', 'volume']].values
                train_y = bit['close'].values
		data = TimeseriesGenerator(train_x, train_y, length=10, batch_size=len(bit))
		
		X = np.array([MinMaxScaler().fit_transform(x) for x in data[0][0]])
		# X = np.array([x for x in data[0][0]])

		Y = data[0][1]
			
		x_train = X[:int(len(X)*0.75)]
		y_train = Y[:int(len(Y)*0.75)]
		x_test  = X[int(len(X)*0.75):]
		y_test  = Y[int(len(X)*0.75):]
		return x_train, y_train, x_test, y_test

if __name__=='__main__':
		prepare_data()
