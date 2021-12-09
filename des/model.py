from prepare_data import prepare_data
import keras 


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
