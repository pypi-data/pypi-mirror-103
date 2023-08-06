
def get_stock_data(tickers, prices = False, financials = False,
                   info = False, recommendations = False):
    import pandas as pd
    import yfinance as yf
    
    information = {}
    tickers = [ticker.lower() for ticker in tickers]
    
    for ticker in tickers:
    
        try:
            if prices == True:
                stock = yf.Ticker(ticker)
                stock = stock.history(period="max")
                information[ticker] = stock
            
            if financials == True:
                stock = yf.Ticker(ticker)
                stock = stock.financials
                information[ticker] = stock
                
            if info == True:
                stock = yf.Ticker(ticker)
                stock = stock.info
                stock = pd.DataFrame.from_dict(stock, orient = "index").T
                information[ticker] = stock
            
            if recommendations == True:
                stock = yf.Ticker(ticker)
                stock = stock.recommendations
                information[ticker] = stock
                
            
            else:
                pass
        except:
            pass
    return information


