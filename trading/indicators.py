import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma: (1darray)
    '''
    #initialization
    ma = []

    # clean 'nan' value part
    for i in range(n-1, stock_price.shape[0]):
        if np.isnan(stock_price[i,0]) == True: # when we find 'nan' value, we delete 'nan' value and the after
            # print('!!!In ma() find nan value at [{}], day {}.'.format(i,i+1))
            stock_price = stock_price[:i, :]
            # print(stock_price)
            break
    days = stock_price.shape[0] # find value of no 'nan' days
    # print('This ma indicator return array from indice {} to {}, i.e. day {} to {}'.format(n-1, days - 1, n, days))

    for i in range(n-1, days): # every loop we add result to the list
        if weights == []:
            ma.append(np.sum(stock_price[i-n+1:i+1, 0]) / n)
        else:
            ma.append(np.dot(np.array(weights), stock_price[i-n+1:i+1, 0]))

    return np.array(ma)



def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (1darray)
    '''
    #initialization
    osc = []


    # clean 'nan' value part
    for i in range(n-1, stock_price.shape[0]):
        if np.isnan(stock_price[i,0]) == True: # when we find 'nan' value, we delete 'nan' value and the after
            # print('!!!In osc() find nan value at [{}], day {}.'.format(i,i+1))
            stock_price = stock_price[:i, :]
            # print(stock_price)
            break
    days = stock_price.shape[0] # find value of no 'nan' days

    # print('This ma indicator return array from indice {} to {}, i.e. day {} to {}'.format(n-1, days - 1, n, days))

    # caculate osc with 'stochastic'
    if osc_type == 'stochastic':
        for i in range(n-1, days): # every loop we add result to the list
            delta = abs(stock_price[i, 0] - min(stock_price[i+1-n:i+1, 0]))
            delta_max = abs(max(stock_price[i+1-n:i+1, 0]) - min(stock_price[i+1-n:i+1, 0]))
            if delta_max == 0:
                osc.append(1)
            else:
                osc.append(delta / delta_max)

    # caculate osc with 'RSI'
    elif osc_type == 'RSI':
        for i in range(n-1, days): # every loop we add result to the list
            days_diff_pos = [] # initialize
            days_diff_neg = []

            # Loop for get lists for postive and neg trend
            for j in range(n-1):
                if stock_price[i-j, 0] - stock_price[i-1-j, 0] > 0:
                    days_diff_pos.append(stock_price[i-j, 0] - stock_price[i-1-j, 0])
                elif stock_price[i-j, 0] - stock_price[i-1-j, 0] < 0:
                    days_diff_neg.append(stock_price[i-j, 0] - stock_price[i-1-j, 0])

            if len(days_diff_neg) == 0: # if the list is empty, return 1 (by limitation)
                osc.append(1)
            elif len(days_diff_pos) == 0: # if the list is empty, return 0 (by limitation)
                osc.append(0)
            else: # caculate osc by using RS
                diff_pos_aver = sum(days_diff_pos) / len(days_diff_pos)
                diff_neg_aver = abs(sum(days_diff_neg) / len(days_diff_neg))
                RS = diff_pos_aver / diff_neg_aver
                osc.append(1 - (1 / (1 + RS)))

    return np.array(osc)
