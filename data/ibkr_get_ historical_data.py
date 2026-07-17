""" 
Script used to pull data from IBKR. Configure the Ticker, Year range and output file path of the csv.
"""

import time
from datetime import datetime, timezone # For UTC timing
# Takes delta of year
from dateutil.relativedelta import relativedelta
# To create new filepath if not exist
from pathlib import Path

import pandas as pd

# Make request to TWS
from ibapi.client import EClient 

# Get response from TWS
from ibapi.wrapper import EWrapper 

# Get specific security to retrieve historicals
from ibapi.contract import Contract

from threading import Thread

# Settings
TICKER_SYMBOL = "SPY"
YEARS_OF_DATA = 20
OUTPUT_FILE = f"data/equities/{TICKER_SYMBOL.lower()}_{YEARS_OF_DATA}y_data.csv"


class IBKRApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self,self)
        self.data = [] # List to store historical data
        self.finished = False # Flag to check when historical data has finished sending

    def historicalData(self, reqId, bar):
        self.data.append({
            'datetime' : bar.date,
            'open' : bar.open,
            'close' : bar.close,
            'high' : bar.high,
            'low' : bar.low,
            'volume' : bar.volume
        })
    
    def historicalDataEnd(self, reqId, start, end):
        self.finished = True # Flag to check if all data of date range is successfully pulled

def run_loop(app):
    app.run()


def get_equity_data(symbol=TICKER_SYMBOL, years=YEARS_OF_DATA, output_file=OUTPUT_FILE):
    app = IBKRApp()
    app.connect('127.0.0.1', 7497, 123) # IP Address points to this computer, 7497 = Paper trading, 7496 = Live Trading
    api_thread = Thread(target=run_loop, args=(app,))
    api_thread.start()
    time.sleep(1)

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'STK'
    contract.exchange = "SMART"
    contract.currency = 'USD'

    # Loop to batch historical data calls to add up to set amount of years
    for i in range(years):
        app.finished = False

        end_dt = datetime.now(timezone.utc) - relativedelta(years=i)
        end_time = end_dt.strftime("%Y%m%d-%H:%M:%S")
    
        app.reqHistoricalData(
            reqId=i + 1,
            contract=contract,
            endDateTime=end_time,
            durationStr='1 Y',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=1,
            formatDate=1,
            keepUpToDate=0,
            chartOptions=[]
        )
        while not app.finished:
            time.sleep(.5)
    app.disconnect()

    df = pd.DataFrame(app.data)
    df = df.drop_duplicates(subset=["datetime"])
    df = df.sort_values("datetime")

    df['return'] = df['close'].pct_change()
    df = df.dropna(subset=['return'])
    
    df = df['datetime,open,high,low,close,volume,return'.split(',')]

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    return df


if __name__ == '__main__':
    get_equity_data()
