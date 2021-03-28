# Evaluate performance.
import numpy as np
import matplotlib.pyplot as plt


def read_ledger(ledger_file, graph = True):
    '''
    Reads and reports useful information from ledger_file.
    '''
    infor_list = []
    with open(ledger_file, 'r') as readfile:
        lines = readfile.readline()
        i = 0
        while lines:
            list = [x for x in lines.split(',')]
            infor_list.append(list)
            lines = readfile.readline()
            i += 1

            if not lines:
                break

    # split first column with element "buy" and "sell" for  counting
    buy_sell_list = []
    for i in infor_list:
        buy_sell_list.append(i[0])
        del i[0]

    infor_array = txt_trans_array(ledger_file)

    num_of_tran = infor_array.shape[0]

    #initialization for ploting graph
    t_linespace = []
    profit_loss = []

    # loop for caculate day-porfit(loss)
    profit_loss_upto_day_t = 0
    for t in range(1825):
        profit_in_day_t = 0
        for i in range(num_of_tran):
            if infor_array[i, 0] == t:
                profit_in_day_t += infor_array[i, -1]
        if profit_in_day_t != 0:
            t_linespace.append(t)
            profit_loss_upto_day_t += profit_in_day_t
            profit_loss.append(profit_loss_upto_day_t)


    # print some relevant overall information
    print('Using strategy {}'.format(ledger_file[7: -4]))
    print('-' * 20)

    print('The total number of "buy" and "sell" transaction are {} and {}.'.format(buy_sell_list.count('buy')
            , buy_sell_list.count('sell')))
    print('The total amount spent and earned over 5 years is {} and {}.'.format(
            round(abs(sum(min(infor_array[i, -1], 0) for i in range(num_of_tran))), 2),
            round(sum(max(infor_array[i, -1], 0) for i in range(num_of_tran)), 2)))
    print('The overall profit(loss) at the final day is {}.'.format(round(
            sum(max(infor_array[i, -1], 0) for i in range(num_of_tran)) +
            sum(min(infor_array[i, -1], 0) for i in range(num_of_tran)), 2))
            )

    # if statment to control whether show the graph
    if graph == True:
        plt.title('Overall profit or loss over 5 years by using {} method.'.format(ledger_file[7: -4]))
        fig1 = plt.plot(t_linespace,profit_loss, label = 'profit or loss')
        plt.legend()
        plt.show()

    print('-' * 20)
    print('\n')







def txt_trans_array(ledger_file):
    # read from ledger_file and put the number in to an array
    # initialization and read file
    infor_list = []
    onedlist = []
    with open(ledger_file, 'r') as readfile:
        lines = readfile.readline()
        i = 0
        while lines:
            list = [x for x in lines.split(',')]
            infor_list.append(list)
            lines = readfile.readline()
            i += 1

            if not lines:
                break

    # split first column with element "buy" and "sell" for  counting
    buy_sell_list = []
    for i in infor_list:
        buy_sell_list.append(i[0])
        del i[0]

    # transform the remaining number readable and put them in an array
    for i in infor_list:
        for j in i:
            onedlist.append(round(float(j.strip('\n')), 2))

    infor_array = np.array(onedlist)
    infor_array = infor_array.reshape((int(len(infor_array) / 5), 5)) # got the data of 2d array

    return infor_array





def txt_trans_buysell(ledger_file):
    # read from ledger_file and return two 2darray buy_array and sell_array with date in first row, price in second row
    # initialization and read file
    infor_list = []
    with open(ledger_file, 'r') as readfile:
        lines = readfile.readline()
        i = 0
        while lines:
            list = [x for x in lines.split(',')]
            infor_list.append(list)
            lines = readfile.readline()
            i += 1

            if not lines:
                break

    # split first column with element "buy" and "sell" for  counting
    buy_sell_list = []
    for i in infor_list:
        buy_sell_list.append(i[0])

    infor_array = txt_trans_array(ledger_file)
    date_array = infor_array[:,0]
    price_array = infor_array[:,-2]

    # sperate 'buy' and 'sell'
    buy_array = np.zeros((2,buy_sell_list.count('buy')))
    sell_array = np.zeros((2,buy_sell_list.count('sell')))
    j = 0
    k = 0
    for i in range(len(buy_sell_list)):

        if buy_sell_list[i] == 'buy':
            buy_array[0, j] = date_array[i]
            buy_array[1, j] = price_array[i]
            j += 1
        elif buy_sell_list[i] == 'sell':
            sell_array[0, k] = date_array[i]
            sell_array[1, k] = price_array[i]
            k += 1

    return buy_array, sell_array



def read_profit(ledger_file):

    infor_array = txt_trans_array(ledger_file)

    return float(sum(infor_array[:, -1]))
