def generate_stock_price(days, initial_price, volatility, Loc=0.0):
    import numpy as np
    '''
    Generates daily closing share prices for a company,
    for a given number of days.
    Loc (float default=0): mean of normal distribution
    '''
    # Initialize stock_prices, initial_price, totalDrift
    stock_prices = np.zeros(days)
    stock_prices[0] = initial_price
    totalDrift = np.zeros(days)
    # Set up the default_rng from Numpy
    rng = np.random.default_rng()
    # Loop over a range(1, days)
    for day in range(1, days):
        inc = rng.normal(loc = Loc)
        # Add stock_prices[day-1] to inc to get NewPriceToday
        NewPriceToday = stock_prices[day - 1] + inc

        # Make a function for the news
        def news(chance, volatility):
            '''
            Simulate the news with %chance
            '''
            # Choose whether there's news today
            news_today = rng.choice([0,1], p=[1-chance, chance])
            duration = rng.integers(3,15)
            # Randomly choose the duration
            news_impact = np.zeros(duration)
            if news_today:
                # Calculate m and drift
                m = rng.normal(0,2)
                drift = m * volatility
                for i in range(duration):
                    news_impact[i] = drift
                return news_impact
            else:
                return news_impact

        # Get the drift from the news
        d = news(0.1, volatility)

        #In-code test
        # print(d)
        # if d[0] != 0:
        #     print("A news happen in day {} and will continue {} days.".format(day,len(d)))
        # Get the duration_time

        duration_time = len(d)
        # Add the drift to the next days
        totalDrift[day : day+duration_time] += d[0]
        # Add today's drift to today's price
        NewPriceToday += totalDrift[day]

        # Set stock_prices[day] to NewPriceToday or to NaN if it's non-postive
        if NewPriceToday <= 0:
            stock_prices[day:] = np.nan
            return stock_prices
        else:
            stock_prices[day] = NewPriceToday
    return np.round(stock_prices, 2)





def get_data(method='read', initial_price=None, volatility=None, finaldate=1824, Loc=0.0):

    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.
    finaldate (int, default 1824): the last day of sotck prices (from 0)
    Loc (float default=0): mean of normal distribution
    '''

    import numpy as np

    #initialize a (1826, 20) size array and a specific size array if initial_price or volatility exist
    whole_sim_data = np.zeros((finaldate+2, 20))
    if initial_price != None:
        num_of_stock = len(initial_price)
        sim_data = np.zeros((finaldate+1, num_of_stock))
    elif volatility != None:
        num_of_stock = len(volatility)
        sim_data = np.zeros((finaldate+1, num_of_stock))


    #generate data with given initial_price and volatility
    if method == 'generate':
        if initial_price != None and volatility != None:
            for i in range(num_of_stock):
                #Assume 5 years = 5*365 = 1825 days
                sim_data[:,i] = generate_stock_price(finaldate+1, initial_price[i], volatility[i], Loc=Loc)
            return sim_data

        #lack argument
        elif initial_price == None and volatility == None:
            return 'Please specify the initial price and volatility for each stock.'
        elif initial_price == None:
            return 'Please specify the initial price for each stock.'
        elif volatility == None:
            return 'Please specify the volatility for each stock.'

    #read data with given initial_price and volatility if they are given
    if method == 'read' :
        #read the whole simulation data
        with open('stock_data_5y.txt', 'r') as readfile:
            lines = readfile.readline()
            i = 0
            while lines:
                num = np.array([float(x) for x in lines.split()])
                whole_sim_data[i, :] = num
                lines = readfile.readline()
                i = i+1

        #situations with different givern argument
        #find whole stock price
        if initial_price == None and volatility == None:
            whole_sim_data = whole_sim_data[1:, :]
            return whole_sim_data

        #find stock price base on initial_price
        elif initial_price != None:
            if volatility != None:
                print('volatility will be ignored')

            price_find = np.zeros(len(initial_price))
            volatility_find = np.zeros(len(initial_price))
            sim_data_g_price = np.zeros([finaldate+2, len(initial_price)])
            #loop for find cloest values
            for i in range(len(initial_price)):
                price_find[i] = whole_sim_data[1, 0]
                volatility_find[i] = whole_sim_data[0, 0]
                sim_data_g_price[:, i] = whole_sim_data[:, 0]

                for j in range(1, 20):
                    if abs(initial_price[i] - price_find[i]) >  abs(initial_price[i] - whole_sim_data[1, j]):
                        price_find[i] = whole_sim_data[1, j]
                        volatility_find[i] = whole_sim_data[0, j]
                        sim_data_g_price[:, i] = whole_sim_data[:, j]

            print('Found data with initial prices', price_find[:], 'and volatilities', volatility_find[:])
            #delete the "volatility" row
            sim_data_g_price = sim_data_g_price[1:, :]
            return sim_data_g_price

        #find stock price base on volatility
        elif initial_price == None and volatility != None:

            price_find = np.zeros(len(initial_price))
            volatility_find = np.zeros(len(initial_price))
            sim_data_g_price = np.zeros([finaldate+2,len(initial_price)])

            #loop for find cloest values
            for i in range(len(volatility)):
                price_find[i] = whole_sim_data[1, 0]
                volatility_find[i] = whole_sim_data[0, 0]
                sim_data_g_price[:, i] = whole_sim_data[:, 0]

                for j in range(1, 20):
                    if abs(volatility[i] - volatility_find[i]) >  abs(volatility[i] - whole_sim_data[0, j]):
                        price_find[i] = whole_sim_data[1, j]
                        volatility_find[i] = whole_sim_data[0, j]
                        sim_data_g_price[:, i] = whole_sim_data[:, j]

            print('Found data with initial prices', price_find[:], 'and volatilities', volatility_find[:])
            #delete the "volatility" row
            sim_data_g_price = sim_data_g_price[1:, :]
            return sim_data_g_price
