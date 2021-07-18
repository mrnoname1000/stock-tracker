#!/usr/bin/env python3

import numpy as np

def obv(df):
    return (np.sign(df["Close"].diff()) * df["Volume"]).cumsum().to_numpy()[-1]
