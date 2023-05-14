import yfinance as yf
import datetime
import pandas as pd
df = pd.read_excel('AICP_LT.xlsx', index_col='Symbol')
df['close']=0
def data():
    for tickerSymbol in df.index:

        start_date = datetime.datetime.now()- datetime.timedelta(days=365)
        end_date = datetime.datetime.now()
        stock = yf.download( tickerSymbol+ '.NS', start=start_date,
                                        end=end_date, interval='1d')
        df['close']=stock['Close'][len(stock)-1]
    df.to_excel('AICP_LT.xlsx')
        
 