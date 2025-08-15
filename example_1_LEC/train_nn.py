import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

# loda data
with open("data and figure/data_train_input.json", "r") as f:
    x = np.array(json.load(f))
with open("data and figure/data_train_output.json", "r") as f:
    y = np.array(json.load(f))

# split into 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# construct the NN model
model = Sequential()
model.add(Dense(64, input_dim=x_train.shape[1], activation='relu'))  
model.add(Dense(64, activation='relu'))
model.add(Dense(2, activation='linear'))  

model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# train the model
history = model.fit(x_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=0)

# save the model
model.save("data and figure/trained_model.h5")

# test the model
loss = model.evaluate(x_test, y_test)
print(f'Loaded model test loss: {loss}')


