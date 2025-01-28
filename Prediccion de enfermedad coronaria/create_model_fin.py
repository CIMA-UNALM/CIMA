from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def create_model_fin(neurons, optimizer='adam', init_mode='uniform', activation='relu'):
    # Crear modelo
    model = Sequential()
    model.add(Dense(neurons, input_shape=(23,), kernel_initializer=init_mode, activation=activation))
    model.add(Dense(1, kernel_initializer=init_mode, activation='sigmoid'))
    
    # Compilar modelo
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model
