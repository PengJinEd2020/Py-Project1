# Functions to implement our trading strategy.
import numpy as np
from trading import process as proc
from trading import indicators as indic
import matplotlib.pyplot as plt

def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt', finaldate=1824):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file
        finaldate (int, default 1824): the last day of sotck prices (from 0)

    Output: None
    '''
    # clean txt file
    with open(ledger, 'w') as writefile:
        writefile.truncate()

    # initialization
    num_of_stock = stock_prices.shape[1]
    portfolio = proc.create_portfolio([amount]*num_of_stock, stock_prices, fees, ledger)

    rng = np.random.default_rng() #random generator

    # for each stock loop day i with period until to finaldate
    for s in range(num_of_stock):
        # for every stock initialize date: i
        i = 1
        while period*i < finaldate:
            if np.isnan(stock_prices[period*i, s]) == True: # when detect nan value, break and throw all stock go to next stock
                proc.sell(period*i, s, np.zeros((finaldate+1, num_of_stock)), 0, portfolio, ledger)
                break
            elif np.isnan(stock_prices[period*i, s]) == False:
                dowhat = rng.choice(['buy','do_nothing','sell'], p = [1/3, 1/3, 1/3])
                if dowhat == 'buy':
                    proc.buy(period*i, s, amount, stock_prices, fees, portfolio, ledger)
                elif dowhat == 'sell':
                    proc.sell(period*i, s, stock_prices, fees, portfolio, ledger)
            i += 1

    # when final day, need sell all stock if it's not nan value.
    for f in range(num_of_stock):
        if np.isnan(stock_prices[finaldate, s]) == False:
            proc.sell(finaldate, f, stock_prices, fees, portfolio, ledger)






def crossing_averages(stock_prices, SMAperiod=200, FMAperiod=50, SMAweights=[], FMAweights=[], amount=5000, fees=20, ledger='ledger_crossing_averages.txt', graph=True, finaldate=1824):
    '''
    finds the crossing points between SMA and FMA to make buying or selling decisions.
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        SMAperiod (int, default 200): period of the SMA (in days)
        FMAperiod (int, default 50): period of the FMA (in days)
        SMAweights, FMAweights (list, default []): must be of length
            SMAperiod(FMAperiod) if specified. Indicates the weights
            to use for the weighted average. If empty, it means non-
            weighted average.
        amount (float, default 5000): how much we spend on each purchase
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: print error
    '''
    # clean txt file
    with open(ledger, 'w') as writefile:
        writefile.truncate()

    # initialization
    num_of_stock = stock_prices.shape[1]
    portfolio = proc.create_portfolio([amount]*num_of_stock, stock_prices, fees, ledger)

    if SMAperiod < FMAperiod:
        return 'Error with periods (SMAperiod < FMAperiod)'

    for s in range(num_of_stock):
        s_SMA = indic.moving_average(stock_prices[:,s:s+1], n=SMAperiod, weights=SMAweights)
        s_FMA = indic.moving_average(stock_prices[:,s:s+1], n=FMAperiod, weights=FMAweights)[SMAperiod-FMAperiod:]
        # now, s_SMA and s_FMA both start from day 'SMAperiod' and we can start compare

        i = SMAperiod
        sign = [] # a list to record the position of SMA and FMA [>, =, <]:[-1,0,1]

        while i < finaldate:
            if np.isnan(stock_prices[i, s]) == True: # similar with random()
                proc.sell(i, s, np.zeros((finaldate+1,num_of_stock)), 0, portfolio, ledger) # throw it away
                break
            elif np.isnan(stock_prices[i, s]) == False:
                if s_SMA[i-SMAperiod] < s_FMA[i-SMAperiod]:
                    #SMA < FMA Note +1
                    sign.append(1)
                elif s_SMA[i-SMAperiod] > s_FMA[i-SMAperiod]:
                    sign.append(-1)
                else:
                    sign.append(0)

            if i > SMAperiod: # avoid only one element in list s.t. can't find sign[-2]
                if sign[-1] - sign[-2] > 0:
                    proc.buy(i, s, amount, stock_prices, fees, portfolio, ledger)
                elif sign[-1] - sign[-2] < 0:
                    proc.sell(i, s, stock_prices, fees, portfolio, ledger)

            i += 1

    # when final day, need sell all stock if it's not nan value.
    for f in range(num_of_stock):
        if np.isnan(stock_prices[finaldate, s]) == False:
            proc.sell(finaldate, f, stock_prices, fees, portfolio, ledger)

            


def momentum(stock_prices, period=200, minimum_cool_down_period=10, overvalued_threshold=[0.7, 0.8], undervalued_threshold=[0.2, 0.3], osc_method='stochastic', amount=5000, fees=20, ledger='ledger_momentum.txt', finaldate=1824):

    '''
    uses a given oscillator (stochastic or RSI) to make buying or selling decisions,
    depending on a low threshold and a high threshold.
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 200): period of stochastic or RSI indicators (in days)
        minimum_cool_down_period (int, default 10): days that can't make any decision after make a decision (in days)
        overvalued_threshold (list default=[0.7, 0.8]): when the oscillator is in this threshold, it's good time to sell.
        undervalued_threshold (list default=[0.2, 0.3]): when the oscillator is in this threshold, it's good time to buy.
        amount (float, default 5000): how much we spend on each purchase
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''

    # clean txt file
    with open(ledger, 'w') as writefile:
        writefile.truncate()

    # initialization
    num_of_stock = stock_prices.shape[1]
    portfolio = proc.create_portfolio([amount]*num_of_stock, stock_prices, fees, ledger)

    for s in range(num_of_stock):
        # initialize
        i = period
        s_osc = indic.oscillator(stock_prices[:, s:s+1], n = period, osc_type = osc_method)
        while i < finaldate:
            if np.isnan(stock_prices[i, s]) == True: # similar with random()
                proc.sell(i, s, np.zeros((finaldate+1,num_of_stock)), 0, portfolio, ledger)
                break

            if s_osc[i-period] > overvalued_threshold[0] and s_osc[i-period] < overvalued_threshold[1]:
                proc.sell(i, s, stock_prices, fees, portfolio, ledger)
                i = i + minimum_cool_down_period - 1 # skip some days if we bought or sold
            elif s_osc[i-period] > undervalued_threshold[0] and s_osc[i-period] < undervalued_threshold[1]:
                proc.buy(i, s, amount, stock_prices, fees, portfolio, ledger)
                i = i + minimum_cool_down_period - 1 # skip some days if we bought or sold

            i += 1

    # when final day, need sell all stock if it's not nan value.
    for f in range(num_of_stock):
        if np.isnan(stock_prices[finaldate, s]) == False:
            proc.sell(finaldate, f, stock_prices, fees, portfolio, ledger)
