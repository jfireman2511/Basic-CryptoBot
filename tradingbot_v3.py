API_KEY = 
API_SECRET = 

import pandas as pd
from wazirx_sapi_client.rest import Client
import ta
from datetime import timedelta
import time


client = Client(api_key=API_KEY, secret_key=API_SECRET)


current_time= str(int(time.time()))
starttime=str(int(current_time)-1800000)


def getdata():
    values_list = client.send("klines", {"symbol":"ethinr", "interval":"15m", "startTime":starttime,"endTime":current_time,"limit":"2000"})
    finalval = values_list[1]
    frame = pd.DataFrame(finalval)
    selected_data = frame.iloc[:, 1:6]
    frame = selected_data.iloc[:, 0:5]
    frame.columns = ['Time', 'Open','High','Low','Close']
    frame.set_index('Time', inplace = True)
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame

df = getdata()
print (df)

def indicators(df):
    df['SMA_20']= ta.trend.sma_indicator(df.Close, window = 20)
    df['stochrsi_k']= ta.momentum.stochrsi_k(df.Close,window=10)
    df.dropna(inplace= True)
    df['Buy']= (df.stochrsi_k<0.09)
    return df
y = indicators(df)
print(y)


file = open("buysell.txt", "a+")

if True in df.values:
    file.write("BUY ORDER MUST BE PLACED\n")
else:
    file.write("NO ORDER MUST BE PLACED YET\n")
