import csv
# from urllib.request import urlopen # stupid python 3 
import urllib2 # python 2
import scipy as sc
import numpy as np
from matplotlib.pyplot import *
from scipy import stats as st
"""General stock array structure is [open, high, low, close, volume] 
   Script takes 250 days worth of stock data per stock, from Google, 
   and calculates the ADL.

   Author:  Douglass Murray
   Date:  2015-12-16
"""

# Simple Moving Average, helper function
def sma(cummulated_data, time_frame):
	"""Calculates the X-day simple moving average, based on:
	   evolving sum(a[:time_frame]) / time_frame

	   Args:
	      cummulated_data: 1D array with close values
	      time_frame: number of days sma average is based on, usually 12, 26, or 9
	   Returns:
	      smas: 1D array with sma values
	"""
	smas = np.array([])
	for i, element in enumerate(cummulated_data):
		if (i + time_frame) >= len(cummulated_data):
			break
		else:
			# sma = sum(time_frame packet) / time_frame 
			sma_element = (sum(cummulated_data[i:time_frame+i]) / time_frame)
			smas = np.append(smas, sma_element)

	return smas

# Exponential Moving Average
def ema(data_set, time_frame):
	"""Calculates the X-day exponential moving average, based on:
	   inital X-day sma * multiplier= inital ema
	   (close - ema(previous_close)) * multiplier + ema(previous_close)

	   Args:
	      data_set: 1D array with close values
	      time_frame: number of days ema average is based on, usually 12, 26 or 9
	   Returns:
	      emas: 1D array with ema values
	"""
	# Multiplier can also be set as a constant decimal percentage (0.18 = 18%)
	multiplier = 2. / (time_frame + 1.)
	# The inital ema is based on the first sma: close - inital_sma * multiplier + inital_sma
	first_sma = sma(data_set, time_frame)
	emas = np.array([data_set[0] - first_sma[0] * multiplier + first_sma[0]])
	
	for i, element in enumerate(data_set):
		# ema = close - previous_ema * multiplier + previous_ema
		ema_element = element - emas[i] * multiplier + emas[i]
		emas = np.append(emas, ema_element)

	# Remove first ema, for plotting purposes
	emas = emas[1:]
	return emas

# Daily Money Flow Multiplier (MFM)
def mfm(daily_data):
	"""Finds daily money flow multiplier (MFM), represented by:
	   ((close - low) - (high - close)) / (high - low)

	   Args:
	      daily_data: 2D array with [open, high, low, close, volume] per row
	   Returns:
	      1D array with [mfm] values
	"""
	closes = daily_data[:,3]
	lows = daily_data[:,2]
	highs = daily_data[:,1]
	mfms = np.array([])
	for i, data in enumerate(daily_data):
		""" ((close - low) - (high - close)) / (high - low)"""
		mfm_value = ((closes[i] - lows[i]) - (highs[i] - closes[i])) / (highs[i] - lows[i])
		mfms = np.append(mfms, mfm_value)
		
	return mfms

# Helper function, Money Flow Volume (MFV)
def mfv(mfm_data, daily_data):
	"""Finds mfv, represented by:
	   (daily mfm * volume)
	
	   Args: 
	      mfm_data: 1D array with [mfm] values
	      daily_data: 2D array with [open, high, low, close, volume] per row
	   Returns:
	      1D array with [mfv] values
	"""
	volumes = daily_data[:,4] #daily_data[i][4]
	mfv = np.array([])
	for i, data in enumerate(mfm_data):
		""" mfm * volume"""
		mfv_value = data * volumes[i]
		mfv = np.append(mfv, mfv_value)
	return mfv


# Daily Accumulation Distribution Line (ADL)
def adl(mfv_data):
	"""Finds daily accumulation distribution line (adl), represented by:
	   previous adl + (current mfv)

	   Args:
	      mfv_data: 1D array with daily mfv data
	   Returns:
	      1D array of daily ADL
	"""
	adl = np.array([])
	for i, data in enumerate(mfv_data):
		adl_value = data + (mfv_data[i-1])
		adl = np.append(adl, adl_value)
	return adl

# Exponenital distribution
def exponential_dist(daily_data, time_interval):
	"""Calculates the exponential distribution.

	   Args:
	      daily_data: 2D stock array with [open, high, low, close, volume]
	      per row
	      time_interval: float representing how many days for interval
	   Returns:
	      exponential_distro: exponential dist array
	"""
	time_range = (250. - time_interval) # 250 is the final time in days
	average_rate = (daily_data[250][3] - daily_data[time_range][3]) / time_interval

	exponential_distro = np.array([])
	for i in range(int(time_interval)):
		expo_value = average_rate * np.exp(-average_rate * (i+1))
		exponential_distro = np.append(exponential_distro, expo_value)
	# print(average_rate)
	return exponential_distro

# Gather stock data from online
# url = 'http://www.google.com/finance/historical?output=csv&q=mu'
# response = urlopen(url) # stupid python 3
# response = urllib2.urlopen(url) # python 2
# data = sc.genfromtxt(response, delimiter=',')

# Or Local stock gather data for when offline
with open('mu.csv', 'rb') as csvfile:
	data = sc.genfromtxt(csvfile, delimiter=',')

# Remove NAN data in array (first row and then first column),
# flip so most recent (which is at the front) is placed at end
data = np.delete(data, 0 , 0) 
data = np.delete(data, 0 , 1)
data = np.flipud(data)
print(data)

# Daily MFM
daily_mfms = mfm(data)
print(daily_mfms)
mfms_x = np.arange(0, len(daily_mfms))
# print(mfms_x)

# Daily MFV
daily_mfvs = mfv(daily_mfms, data)
print(daily_mfvs)
mfvs_x = np.arange(0, len(daily_mfvs))
# print(mfvs_x)

# ADL
daily_adls = adl(daily_mfvs)
print(daily_adls)
adls_x = np.arange(0, len(daily_adls))
# print(adls_x)

# EMA
daily_closes = data[:,3]
ema_12_day = ema(daily_closes, 12)
ema_26_day = ema(daily_closes, 26)

# Plot stock price
# Polynomial fit
data_x = np.arange(0, data.shape[0])
coefficients_data = np.polyfit(data_x, data[:,3] , 12)
polynomial_data = np.poly1d(coefficients_data)
ys_data = polynomial_data(data_x)
plot(data_x, data[:,3], 'o')
plot(data_x, ys_data)
ylabel('Stock Price (USD)')
xlabel('Days')
show()
print(coefficients_data)
print(polynomial_data)

# Plot graph of daily MFMs
plot(mfms_x, daily_mfms, 'o')
# plot(x, ys)
ylabel('Money Flow Multiplier (MFM)')
xlabel('Days')
# xlim(-10, 10)
ylim(-1.25, 1.25)
show()

# Plot graph of daily MFVs
# Polynomial fit
coefficients_mfv = np.polyfit(mfvs_x, daily_mfvs, 6)
polynomial_mfv = np.poly1d(coefficients_mfv)
ys_mfv = polynomial_mfv(mfvs_x)
plot(mfvs_x, daily_mfvs, 'o')
plot(mfvs_x, ys_mfv)
ylabel('Money Flow Volume (MFV)')
xlabel('Days')
show()
print(coefficients_mfv)
print(polynomial_mfv)

# Plot graph of daily ADLs
# Polynomial fit
coefficients_adl = np.polyfit(adls_x, daily_adls, 12)
polynomial_adl = np.poly1d(coefficients_adl)
ys_adls = polynomial_adl(adls_x)
plot(adls_x, daily_adls, 'o')
plot(adls_x, ys_adls)
ylabel('Accumulation Distribution Line (ADL)')
xlabel('Days')
show()
print(coefficients_adl)
print(polynomial_adl)

# Overlay stock price graph with ADL graph
# First plot stock price with poly fit
fig, ax1 = subplots()
ax1.plot(data_x, data[:,3], 'b-')
# ax1.plot(data_x, ys_data, 'b-') # Poly fit
ax1.set_xlabel('Days')
ax1.set_ylabel('Stock Price (USD)', color='b')
# Set y axis tick labels to proper graph color
for tl in ax1.get_yticklabels():
	tl.set_color('b')

# Second plot ADL with poly fit
ax2 = ax1.twinx()
ax2.plot(data_x, daily_adls, 'g-') # Note x axis is the same
# ax2.plot(data_x, ys_adls, 'g-') # Note x axis is the same (poly fit)
ax2.set_ylabel('Accumulation Distribution Line (ADL)', color='g')
# Set y axis tick labels to proper graph color
for tl in ax2.get_yticklabels():
	tl.set_color('g')
show()

# Plotting Stock price with EMA overlay
fig, ax1 = subplots()
# ax1.plot(data_x, data[:,3], 'b-')
ax1.plot(data_x, ys_data, 'b-') # Poly fit
ax1.set_xlabel('Days')
ax1.set_ylabel('Stock Price (USD)', color='b')
# Set y axis tick labels to proper graph color
for tl in ax1.get_yticklabels():
	tl.set_color('b')

ax2 = ax1.twinx()
ax2.plot(data_x, ema_12_day, 'r-') # Note x axis is the same
# ax2.plot(data_x, ys_adls, 'r-') # Note x axis is the same (poly fit)
ax2.set_ylabel('Exponential Moving Average (EMA)', color='r')
# Set y axis tick labels to proper graph color
for tl in ax2.get_yticklabels():
	tl.set_color('r')
show()

# r-squared of ADL and poly fit of ADL
adl_lingress_slope, adl_lingress_intercept, adl_lingress_rvalue, adl_lingress_pvalue, adl_lingress_stderr = st.linregress(daily_adls, ys_adls)
r_squared = adl_lingress_rvalue**2.
print("ADL r^2: %f" %r_squared)


"""
# Exponential distribution section
time_range = 250.
exp_function = exponential_dist(data, time_range)
print(exp_function)
plot(range(int(time_range)), exp_function, 'o')
ylabel('Exponential Probability')
xlabel('Days')
show()

# Overlay stock price graph with Exponential graph
# Plot stock price with poly fit
fig, ax1 = subplots()
ax1.plot(data_x[1:], data[1:,3], 'b-')
# ax1.plot(data_x, ys_data, 'b-') # Poly fit
ax1.set_xlabel('Days')
ax1.set_ylabel('Stock Price (USD)', color='b')
# Set y axis tick labels to proper graph color
for tl in ax1.get_yticklabels():
	tl.set_color('b')

# Plot Exponential
ax2 = ax1.twinx()
ax2.plot(data_x[1:], exp_function, 'g-') # Note x axis is the same
ax2.set_ylabel('Exponential Probability', color='g')
# Set y axis tick labels to proper graph color
for tl in ax2.get_yticklabels():
	tl.set_color('g')
show()
"""

# TODO: Blessings terminal based version
# is it possible to do graphs in terminal with blessings?!
# maybe use termgraph.py by mkaz?
# Add MACD (moving average convergence/divergence oscillator) plot with stock prices
# Add plotting helper function maybe