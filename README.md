# StockMarketAnalysis
Dashboard (Single Page Application) that shows some basic information about the Stock market like top gainers , top losers , today's business news etc. 

We can also view historical data of any company listed in the Stock Market (NSE or BSE) between the given dates, for this feature we have used APIs like NSEpy and nsetools which provide historical time series data for no cost.

Also has the functionality of performing timeseries analysis on historical Stock Market Data.

Some of the libraries we used in this project are numpy, pandas, matplotlib, plotly, dash, nsetools, nsepy, statsmodels, pmdarima, sklearn.

We also attempted to build a feature of realtime forecasting for a particular selected company stock. i.e. As the we know the Stock market is live during the weekdays and the value of Stocks usually changes every few seconds. We had attempted to build a feature that accepts these new values and updates the model based on the updated data. As the model changes , the forecast also changes according to the new data and plots the updated forecast. The forecast graph scrolls forward as new data arrives at regular intervals.
