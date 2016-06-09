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

hist2 = pandas.DataReader(SYMBOL, 'yahoo', date_start, date_stop)
hist_high = np.array(hist['High'].tolist())

hist3 = pandas.DataReader(SYMBOL, 'yahoo', date_start, date_stop)
hist_low = np.array(hist['Low'].tolist())

hist4 = pandas.DataReader(SYMBOL, 'yahoo', date_start, date_stop)
hist_close = np.array(hist['Close'].tolist())

# History for testing the SVM
date_start = date.datetime(2006, 6, 28)
date_stop = date.datetime(2011, 6, 20)
hist = pandas.DataReader(SYMBOL, 'yahoo', date_start, date_stop)

sma_5 = ta.SMA(hist_train, timeperiod=5)
sma_60 = ta.SMA(hist_train, timeperiod=60)

#From Research Paper:
#Buying rule: 5-simple moving average crosses up 60-simple moving average
#Selling rule: 5-simple moving average crosses down 60-simple moving average
buy_day = []
buy_value = []
sell_day = []
sell_value = []
crossover = False
for i in range(len(hist_train)):
    if ( (sma_5[i] > sma_60[i]) and
         (crossover == False) ):

        #need to skip first crossover
        buy_day.append(i)
        buy_value.append(hist_train[i])
        #print "Long: Day " + str(i) + " Value = " + str(hist_train[i])
        crossover = True

    elif ( (sma_5[i] < sma_60[i]) and
           (crossover == True) ):

        sell_day.append(i)
        sell_value.append(hist_train[i])
        #print "Exit: Day " + str(i) + " Value = " + str(hist_train[i])
        crossover = False


#collect data about results to compare to table 2 of research paper
#need Sum and avg of return, earning(,) and loss...(oxford comma or no?)
#need success rate and others but fuck it.
trades = []
returns = [] #raw
success = 0 #number of winning trades
successVal = 0 #total winnings
fail = 0    #number of loosing trades
failVal = 0 #total losses

for buy, sell in zip(buy_value, sell_value): 
    trades.append(sell - buy)
    returns.append(float(sell - buy)/float(buy))

for result, ret in zip(trades, returns):
    #print "Trade: " + str(result)
    if result > 0:
        success = success + 1
        successVal = successVal + result
    else:
        fail = fail + 1
        failVal = failVal + result

winRate = float(success)/float(success + fail)
avgWin = float(successVal)/float(success)
avgLoss = float(failVal)/float(fail)
avgRet = float(sum(returns))/float(sum(buy_value))

#for comparison with table 2 of paper:
print "Sum Return: " + str(sum(returns))
print "Avg Return: " + str(avgRet)
print "Avg Earning: " + str(avgWin)
print "Avg Loss: " + str(avgLoss)
print "Sum Earning: " + str(successVal)
print "Sum Loss: " + str(failVal)
print "Success Rate: " + str(winRate)


#Lets paint happy figures
#plt.plot(hist_train, 'r-', label='Raw')
#plt.plot(sma_5, 'g-', label='SMA = 5')
#plt.plot(sma_60, 'b-', label='SMA = 60')
#for each in buy_day:
#    plt.plot(each, hist_train[each], 'ro')
#for item in sell_day:
#    plt.plot(item, hist_train[item], 'bo')
#plt.xticks(range(0, len(hist_train), 100))
#plt.legend(loc='upper left')
#plt.xlabel("Trading Days")
#plt.ylabel("Adj Close")
#plt.show()


#begin svm work for part 2
#first construct technical indicators to classify svm
#we need RAVI, ADX, K&D, RSI, MACD

ravi = []
sma_7 = ta.SMA(hist_train, timeperiod=7)
sma_65 = ta.SMA(hist_train, timeperiod=65)

for s, l in zip(sma_7, sma_65):
    raviVal =abs(100 * (float(s) - float(l)) / l)
    ravi.append(raviVal)

tp = 14
x = 0

adx = ta.ADX(hist_high, hist_low, hist_close, timeperiod=14)

slowk, slowd = ta.STOCH(hist_high, hist_low, hist_close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

rsi = ta.RSI(hist_close, timeperiod=14)

macd, macdsignal, macdhist = ta.MACD(hist_close, fastperiod=12, slowperiod=26, signalperiod=9)
