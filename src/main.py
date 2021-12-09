import numpy as np
import keras 
import pandas as pd
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler
def prepare_data(train_size=0.80):
    bit = pd.read_csv('/kaggle/input/bitcoin-data/bitcoin_data.csv', sep=',')
    
    train_x = bit[['open', 'high', 'low', 'close', 'Volume BTC']].values
    train_y = bit['close'].values
    data = TimeseriesGenerator(train_x, train_y, length=10, batch_size=len(bit))

    X = np.array([MinMaxScaler().fit_transform(x) for x in data[0][0]])
    # X = np.array([x for x in data[0][0]])

    Y = data[0][1]

    x_train = X[:int(len(X)*train_size)]
    y_train = Y[:int(len(Y)*train_size)]
    x_test  = X[int(len(X)*train_size):]
    y_test  = Y[int(len(X)*train_size):]
    return x_train, y_train, x_test, y_test
    
if __name__ == '__main__':
    x_train, y_train, x_test, y_test = prepare_data()
    dim_input = x_train[1].shape
    # Declaracion modelo
    model = keras.Sequential()       

    # primera capa oculta
    model.add(keras.layers.Dense(128))

    # segunda capa oculta: biderecctional lstm la backward layer es la misma si no se especifica
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(256, return_sequences=True), merge_mode='sum'))

    # Tercera capa oculta: lstm
    model.add(keras.layers.LSTM(256))


    # Cuarta capa oculta: dense
    model.add(keras.layers.Dense(128))

    model.compile(optimizer='adam', loss='mean_squared_error')
    history = model.fit(x_train, y_train, epochs=100, batch_size=16, verbose=1)
    model.save('modelo.h5')
