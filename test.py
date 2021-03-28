import numpy as np
import trading.data as data
import trading.process as process
import trading.indicators as indicators
import trading.strategy as strategy
import trading.performance as performance
import matplotlib.pyplot as plt

stock_prices = data.get_data(method='read', initial_price=[150, 200, 300, 400])

strategy.crossing_averages(stock_prices)
strategy.momentum(stock_prices)
