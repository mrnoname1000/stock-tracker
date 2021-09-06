import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("webagg")

from matplotlib.pylab import rcParams

from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LSTM, Dropout, Dense

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from . import constants

import json


def sliding_window(data, window_length):
    x = []

    for i in range(window_length, len(data)):
        _x = data[i - window_length : i]
        x.append(_x)

    return np.array(x)


def new_model(window_size=60):
    model = keras.Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(window_size, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss="mean_squared_error", optimizer="adam")

    return model


def train(model, df, scaler, window_size=60):
    # normalize
    dataset = scaler.transform(df.values)

    x = sliding_window(dataset, window_size)
    y = dataset[window_size:]

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=2 / 3, shuffle=False)

    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=1)

    return model


def predict(model, df, scaler, window_size=60):
    assert window_size < len(df)

    inputs = df.iloc[-window_size * 2 :]
    inputs = inputs.values
    inputs = scaler.transform(inputs)
    inputs = sliding_window(inputs, window_size)

    predictions = model.predict(inputs)
    predictions = scaler.inverse_transform(predictions)

    output = df.copy(deep=True)
    output.append(
        pd.DataFrame(
            index=pd.date_range(output.index[-1] + pd.Timedelta(1, "day"), periods=window_size)
        )
    )
    output["Predictions"] = np.concatenate(
        ([[np.nan]] * (len(output) - len(predictions)), predictions)
    )
    print(output)

    plt.plot(output[["Close"]])
    plt.plot(output[["Predictions"]])
    plt.show()
