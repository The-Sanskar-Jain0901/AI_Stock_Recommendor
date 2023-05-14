import datetime
import pandas as pd
import numpy as np
import pandas as pd
import yfinance as yf


def pivots():
    stock_data = pd.read_excel('AICP_LT.xlsx')

    for tickerSymbol in stock_data['Symbol']:
        start_date = datetime.datetime.now() - datetime.timedelta(days=60)
        end_date = datetime.datetime.now() - datetime.timedelta(days=30)
        stock = yf.download(tickerSymbol + '.NS', start=start_date,
                            end=end_date, interval='1mo')
        p = (stock.iloc[0]['High']+stock.iloc[0]
             ['Low']+stock.iloc[0]['Close'])/3
        stock_data.loc[stock_data['Symbol'] == str(
            tickerSymbol), 'R1'] = p*2-stock.iloc[0]['Low']
        stock_data.loc[stock_data['Symbol'] == str(
            tickerSymbol), 'R2'] = p+stock.iloc[0]['High']-stock.iloc[0]['Low']
        stock_data['R1.5'] = (stock_data['R1']+stock_data['R2'])/2
        stock_data['R1.25'] = (stock_data['R1']+stock_data['R1.5'])/2
    stock_data.to_excel("AICP_LT.xlsx")
pivots()