The goal of this project is to harvest volatility risk premium (VRP) in SP500 by implementing GARCH and its variants to statistically predict the historical volatility (HV). The VRP is calculated by subtracting implied volatility (IV) from historical volatility (HV). I will be using the VIX as a proxy for IV.

Definitions:
- IV is a forecast on how volatie the price of the underlying asset may be in the future, but it is calculated from the market price of the option itself. It defers from HV because HV is calculated from the historical price of underlying asset and not the option price. This means that IV includes the premiums that traders are willing to accept to hedge themselves against uncertainty.

Volatility Cluster Modelling:
1. Pull 10 years of SPY price data from Alpaca
2. Split into train test set
3. Deploy a GARCH model to forecast the 30 day realised Volatility (RV) of SPY
4. Calculate Realised Volatility of SPY for ground truth (a and b are optional)
    a. close to close volatility - check against CBOE Realised Vol (ticker: RVOL)
    b. Parkinson or Garman-Klass Volatility (accounts for intrday volatility by using OHLC instead of just close to close data)
5. Model Validation on test set
    a. Root Mean Squared Error/ Mean Absolute Error for model accuracy
    b. Diebold-Mariano Test for comparing 2 forecasting models
6. Iterate through steps 3 and 5 with different variants of GARCH
7. Calculate the VRP using the best model's forecasts against VIX

Future direction - Algo Trading Strategy:
1. Research how VRP can be harvested using options
    a. Delta Neutral Straddles
    b. Covered Calls/ Cash Puts
    c. Variance Swaps (Remeber to square volatility)
2. Create a strategy class to develop algorithmic trading strategies
3. Create a backtesting class for backtesting strategies
4. Measure sharpe, max drawdowns, volatility and YOY returns

Additional Filters to develop:
1. Sector Rotation - Relative Rotation Graph (Warning: all sectors could be crashing but a sector can be crashing less, and be placed in the "leading" qudrant and not "lagging")
2. Market Regime - HMM/GMM/CJM
    a. Feature Engineering using PCA and Random Matrix Theory (RMT)
    b. Features would include (VRP, IV, 50SMA, 200SMA, Interest Rates, 2-10 T-bill yields, CPI, PPI, NFP, unemployment, DXY, XAUUSD)
3. Factor decomposition of Hedge Fund's portfolio to find their factor tilts


To start env
Go to Terminal and type:
1) conda env update -f environment.yml --prune
2) conda activate TradingLab-venv