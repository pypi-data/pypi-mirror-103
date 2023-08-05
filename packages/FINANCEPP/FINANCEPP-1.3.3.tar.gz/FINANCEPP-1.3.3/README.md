Documentation of the "CovidResilience" package

The purpose of the package is, given a list of stock tickers, to state what are the most covid resilient stocks and what are the worst ones.
It computes a very simple score based on the volatility and return of the stocks over different periods of time.


CovidResilience(stock_index = "STOXX 600", start_date = "2020-01-19", end_date = "2021-01-19", tickers = None)


Input: 

- stock_index : benchmark  (example : "CAC 40","S&P 500", "STOXX 600")
- start_date, end_date : strings, format "YYYY-MM-DD"
- tickers : list of tickers


Output:

- .relevant_data
- .relevant_data_returns
- .volatilities
- .rslt


Example (copy/paste):

!pip install FINANCEPP

from finance import covidresilient as cr

list_of_tickers = ["FP.PA","MC.PA","AI.PA","OR.PA", "RI.PA","AIR.PA"]

covidfilter = cr.CovidResilience("CAC 40","2020-01-19", "2021-01-19", tickers = list_of_tickers)

covidfilter.run()

covidfilter.rslt

Note that some of the tickers may not be the ones that are used by yahoo finance. Make sure you use the proper tickers.