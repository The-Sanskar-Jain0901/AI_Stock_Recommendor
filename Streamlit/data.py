import datetime
import yfinance as yf
import pandas as pd
stock_data = pd.read_excel('AICP_LT.xlsx',index_col='Symbol')
stock_data['close']=0
def data():
        for tickerSymbol in stock_data.index:

            start_date = datetime.datetime.now()- datetime.timedelta(days=365)
            end_date = datetime.datetime.now()
            stock = yf.download(tickerSymbol + '.NS', start=start_date,
                                end=end_date, interval='1d')
            
            stock_data.loc[str(tickerSymbol) == stock_data.index,
                    'close'] =stock['Close'][len(stock)-1]
            
        stock_data.to_excel("AICP_LT.xlsx")

      
    
        
            
            