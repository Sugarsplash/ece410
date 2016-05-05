"""
	Black-scholes code converted from matlab

	Programmed by William Harrington
	wrh2.github.io
"""

from math import log, erfc, sqrt, exp

def blackscholes(stockprice, strike, riskfree, time, volatility):
	d1 = (log(stockprice/strike)+(riskfree+.5*volatility**2)*time)/(volatility*sqrt(time))
	d2 = d1 - volatility*sqrt(time)

	callprice = stockprice*.5*erfc(-d1/sqrt(2))-strike*exp(-riskfree*time)*.5*erfc(-d2/sqrt(2))

	putprice = strike*exp(-riskfree*time)*.5*erfc(d2/sqrt(2))-stockprice*.5*erfc(d1/sqrt(2))

	calldelta = .5*erfc(-d1/sqrt(2))

	putdelta = calldelta - 1

	return [callprice, putprice, calldelta, putdelta]
