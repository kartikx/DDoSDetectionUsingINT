import pickle
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

with open("serializedData/x_train_data", "rb") as f:
    x_train = pickle.load(f)

with open("serializedData/y_train_data", "rb") as f:
    y_train = pickle.load(f)

# with open("serializedData/x_test_data", "rb") as f:
#     x_test = pickle.load(f)

# with open("serializedData/y_test_data", "rb") as f:
#     y_test = pickle.load(f)

with open("capturedData/x_train_data_1", "rb") as f:
    x_test = pickle.load(f)

with open("capturedData/y_train_data_1", "rb") as f:
    y_test = pickle.load(f)


print(len(x_train), len(y_train), len(x_test), len(y_test))
print(x_train.shape)
"""
Need to reshape, because each example must have a sequence.
Note: Is this correct approach? Should I instead think more deeply
about what the time series actually is like?
"""
x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])
y_train = y_train.reshape(y_train.shape[0], 1, 1)

x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])
y_test = y_test.reshape(y_test.shape[0], 1, 1)

# Recurrent Model

model = keras.Sequential()

# The first index is the number of timesteps, and the second is the dimension of the feature.
model.add(keras.Input(shape=(None, 4)))

model.add(keras.layers.SimpleRNN(128, activation='relu'))
# model.add(keras.layers.Dense(32, activation="relu"))
model.add(keras.layers.Dense(2, activation="softmax"))

print(model.summary())

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(),
    optimizer=keras.optimizers.Adam(learning_rate=0.00001),
    metrics=["accuracy"]
)

model.fit(x_train, y_train, batch_size=64, epochs=15)

model.evaluate(x_test, y_test)