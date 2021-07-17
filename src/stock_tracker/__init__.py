import time

import numpy as np
import pandas as pd
import yfinance as yf

from get_all_tickers import get_tickers as gt

def main():
    stocks = gt.get_tickers_filtered(mktcap_min=50000)
    tickers = yf.Tickers(stocks).tickers
    histories = {stock: ticker.history(period="max") for stock, ticker in tickers.items()}

    # OBV analysis
    obv_df = pd.DataFrame(columns=["OBV"])
    timeframe = 10 # number of days to look at

    for stock, df in histories.items():
        obv = (np.sign(df['Close'].diff()) * df['Volume']).cumsum().to_numpy()[-1]
        obv_df.loc[stock] = obv

    obv_df["Rank"] = obv_df["OBV"].rank(ascending=False)
    obv_df.sort_values("OBV", inplace=True, ascending=False)
    print(obv_df)

    if False:
        list_files = (glob.glob("<Your Path>\\Daily_Stock_Report\\Stocks\\*.csv")) # Creates a list of all csv filenames in the stocks folder
        new_data = [] #  This will be a 2D array to hold our stock name and OBV score
        interval = 0  # Used for iteration
        while interval < len(list_files):
            Data = pd.read_csv(list_files[interval]).tail(10)  # Gets the last 10 days of trading for the current stock in iteration
            pos_move = []  # List of days that the stock price increased
            neg_move = []  # List of days that the stock price increased
            OBV_Value = 0  # Sets the initial OBV_Value to zero
            count = 0
            while (count < 10):  # 10 because we are looking at the last 10 trading days
                if Data.iloc[count,1] < Data.iloc[count,4]:  # True if the stock increased in price
                    pos_move.append(count)  # Add the day to the pos_move list
                elif Data.iloc[count,1] > Data.iloc[count,4]:  # True if the stock decreased in price
                    neg_move.append(count)  # Add the day to the neg_move list
                count += 1
            count2 = 0
            for i in pos_move:  # Adds the volumes of positive days to OBV_Value, divide by opening price to normalize across all stocks
                OBV_Value = round(OBV_Value + (Data.iloc[i,5]/Data.iloc[i,1]))
            for i in neg_move:  # Subtracts the volumes of negative days from OBV_Value, divide by opening price to normalize across all stocks
                OBV_Value = round(OBV_Value - (Data.iloc[i,5]/Data.iloc[i,1]))
            Stock_Name = ((os.path.basename(list_files[interval])).split(".csv")[0])  # Get the name of the current stock we are analyzing
            new_data.append([Stock_Name, OBV_Value])  # Add the stock name and OBV value to the new_data list
            interval += 1
        df = pd.DataFrame(new_data, columns = ['Stock', 'OBV_Value'])  # Creates a new dataframe from the new_data list
        df["Stocks_Ranked"] = df["OBV_Value"].rank(ascending = False)  # Rank the stocks by their OBV_Values
        df.sort_values("OBV_Value", inplace = True, ascending = False)  # Sort the ranked stocks
        df.to_csv("<Your Path>\\Daily_Stock_Report\\OBV_Ranked.csv", index = False)  # Save the dataframe to a csv without the index column

    return 0
