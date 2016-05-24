import pandas_datareader.data as pandas
import datetime as date
import matplotlib.pylab as plt
import talib as ta
import numpy as np

SYMBOL = "600887.SS"

# History for training the SVM
date_start = date.datetime(1999, 6, 14)
date_stop = date.datetime(2006, 6, 27)
hist = pandas.DataReader(SYMBOL, 'yahoo', date_start, date_stop)
hist_train = np.array(hist['Adj Close'].tolist())

# History for testing the SVM
date_start = date.datetime(2006, 6, 28)
date_stop = date.datetime(2011, 6, 20)
hist = pandas.DataReader(SYMBOL, 'yahoo', date_start, date_stop)
hist_test = (hist['Adj Close'].tolist())

sma_6 = ta.SMA(hist_train, timeperiod=6)
sma_65 = ta.SMA(hist_train, timeperiod=65)

buy_day = []
sell_day = []
crossover = False
for i in range(len(hist_train)):
    if ( (sma_6[i] > sma_65[i]) and
         (crossover == False) ):

        buy_day.append(i)
        print("Long: Day {0}".format(i))
        crossover = True

    elif ( (sma_6[i] < sma_65[i]) and
           (crossover == True) ):

        sell_day.append(i)
        print("Exit: Day {0}".format(i))
        crossover = False

#plt.plot(hist_train, 'r-', label='Raw')
plt.plot(sma_6, 'g-', label='SMA = 6')
plt.plot(sma_65, 'b-', label='SMA = 65')
plt.xticks(range(0, len(hist_train), 100))
plt.legend(loc='upper left')
plt.xlabel("Trading Days")
plt.ylabel("Adj Close")
plt.show()
