# runner.py
#!usr/bin/env python27
import csv
# from urllib.request import urlopen # stupid python 3
import urllib2 # python 2
import scipy as sc
import numpy as np
from matplotlib.pyplot import *
from scipy import stats as st
from analysis.startstock import *
from main import *
"""This is the true 'main' script, as it runs all the choices made in main.py.
   The main.py is really the GUI script, where choices are selected by user.

   Args:
      stock: string containing lettered stock choice.  Imported from main.py.

   Author: Douglass Murray
   Date: 2016-03-30
"""
stock = main_terminal()
stock_pick = stock + '.csv'

# Gather stock data from online
url = 'http://www.google.com/finance/historical?output=csv&q=' + stock
# response = urlopen(url) # stupid python 3
response = urllib2.urlopen(url) # python 2
data = sc.genfromtxt(response, delimiter=',')

# Or Local stock gather data for when offline
# with open(stock_pick, 'rb') as csvfile:
	# data = sc.genfromtxt(csvfile, delimiter=',')

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
# ema_26_day = ema(daily_closes, 26)

# MACD
macd = macd(data)
signal_line = ema(macd,9)
macd_histogram = macd - signal_line

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

# Plotting of MACD data
# First MACD line
fig, ax1 = subplots()
# ax1.plot(data_x, data[:,3], 'b-')
ax1.plot(data_x, macd, 'b-') # Poly fit
ax1.set_xlabel('Days')
ax1.set_ylabel('Moving Average C/D Oscillator (MACD)', color='b')
# Set y axis tick labels to proper graph color
for tl in ax1.get_yticklabels():
	tl.set_color('b')

# Then Signal Line
ax2 = ax1.twinx()
ax2.plot(data_x, signal_line, 'r-') # Note x axis is the same
# ax2.plot(data_x, signal_line, 'r-') # Note x axis is the same (poly fit)
ax2.set_ylabel('Exponential Moving Average (EMA)', color='r')
# Set y axis tick labels to proper graph color
for tl in ax2.get_yticklabels():
	tl.set_color('r')

# Finally include MACD Histogram
ax3 = ax2.twinx()
ax3.plot(data_x, macd_histogram, 'g-')
show()

# r-squared of ADL and poly fit of ADL
adl_lingress_slope, adl_lingress_intercept, adl_lingress_rvalue, adl_lingress_pvalue, adl_lingress_stderr = st.linregress(daily_adls, ys_adls)
r_squared = adl_lingress_rvalue**2.
print("ADL r^2: %f" %r_squared)

# TODO: Blessings terminal based version
# is it possible to do graphs in terminal with blessings?!
# maybe use termgraph.py by mkaz?
# Add MACD (moving average convergence/divergence oscillator) plot with stock prices
# Add plotting helper function maybe
