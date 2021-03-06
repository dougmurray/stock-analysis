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
stock_pick = "%s.csv" % stock

# Gather stock data from online
urlbegin = "http://www.google.com/finance/historical?output=csv&q="
url = urlbegin + stock
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

# Plotting all in one figure
fig = figure()

# Plot stock price
# Polynomial fit
data_x = np.arange(0, data.shape[0])
coefficients_data = np.polyfit(data_x, data[:,3] , 12)
polynomial_data = np.poly1d(coefficients_data)
ys_data = polynomial_data(data_x)
print(coefficients_data)
print(polynomial_data)

ax1 = fig.add_subplot(3,3,1)
ax1.plot(data_x, data[:,3], 'o')
ax1.plot(data_x, ys_data)
ylabel('Stock Price (USD)')
xlabel('Days')
title(stock)
# show()

# Plot graph of daily MFMs
ax2 = fig.add_subplot(3,3,2)
ax2.plot(mfms_x, daily_mfms, 'o')
# plot(x, ys)
ylabel('Money Flow Multiplier (MFM)')
xlabel('Days')
title(stock + ' MFM')
# xlim(-10, 10)
ylim(-1.25, 1.25)
# show()

# Plot graph of daily MFVs
# Polynomial fit
coefficients_mfv = np.polyfit(mfvs_x, daily_mfvs, 6)
polynomial_mfv = np.poly1d(coefficients_mfv)
ys_mfv = polynomial_mfv(mfvs_x)
print(coefficients_mfv)
print(polynomial_mfv)

ax3 = fig.add_subplot(3,3,3)
ax3.plot(mfvs_x, daily_mfvs, 'o')
ax3.plot(mfvs_x, ys_mfv)
ylabel('Money Flow Volume (MFV)')
xlabel('Days')
title(stock + ' MFV')
# show()

# Plot graph of daily ADLs
# Polynomial fit
coefficients_adl = np.polyfit(adls_x, daily_adls, 12)
polynomial_adl = np.poly1d(coefficients_adl)
ys_adls = polynomial_adl(adls_x)
print(coefficients_adl)
print(polynomial_adl)

ax4 = fig.add_subplot(3,3,4)
ax4.plot(adls_x, daily_adls, 'o')
ax4.plot(adls_x, ys_adls)
ylabel('Accumulation Distribution Line (ADL)')
xlabel('Days')
title(stock + ' ADL')
# show()

# Overlay stock price graph with ADL graph
# First plot stock price with poly fit
# fig, ax1 = subplots()
ax5 = fig.add_subplot(3,3,5)
ax5.plot(data_x, data[:,3], 'b-')
# ax1.plot(data_x, ys_data, 'b-') # Poly fit
ax5.set_xlabel('Days')
ax5.set_ylabel('Stock Price (USD)', color='b')
title(stock + ' ADL Overlay')
# Set y axis tick labels to proper graph color
for tl in ax5.get_yticklabels():
	tl.set_color('b')

# Second plot ADL with poly fit
ax6 = ax5.twinx()
ax6.plot(data_x, daily_adls, 'g-') # Note x axis is the same
# ax2.plot(data_x, ys_adls, 'g-') # Note x axis is the same (poly fit)
ax6.set_ylabel('Accumulation Distribution Line (ADL)', color='g')
# title(stock)
# Set y axis tick labels to proper graph color
for tl in ax6.get_yticklabels():
	tl.set_color('g')
# show()

# Plotting Stock price with EMA overlay
ax7 = fig.add_subplot(3,3,6)
# fig, ax1 = subplots()
# ax1.plot(data_x, data[:,3], 'b-')
ax7.plot(data_x, ys_data, 'b-') # Poly fit
ax7.set_xlabel('Days')
ax7.set_ylabel('Stock Price (USD)', color='b')
title(stock + ' EMA Overlay')
# Set y axis tick labels to proper graph color
for tl in ax7.get_yticklabels():
	tl.set_color('b')

ax8 = ax7.twinx()
ax8.plot(data_x, ema_12_day, 'r-') # Note x axis is the same
# ax2.plot(data_x, ys_adls, 'r-') # Note x axis is the same (poly fit)
ax8.set_ylabel('Exponential Moving Average (EMA)', color='r')
# title(stock)
# Set y axis tick labels to proper graph color
for tl in ax8.get_yticklabels():
	tl.set_color('r')
# show()

# Plotting of MACD data
# First MACD line
ax9 = fig.add_subplot(3,3,7)
# fig, ax1 = subplots()
# ax1.plot(data_x, data[:,3], 'b-')
ax9.plot(data_x, macd, 'b-') # Poly fit
ax9.set_xlabel('Days')
ax9.set_ylabel('Moving Average C/D Oscillator (MACD)', color='b')
title(stock + 'MACD')
# Set y axis tick labels to proper graph color
for tl in ax9.get_yticklabels():
	tl.set_color('b')

# Then Signal Line
ax10 = ax9.twinx()
ax10.plot(data_x, signal_line, 'r-') # Note x axis is the same
# ax2.plot(data_x, signal_line, 'r-') # Note x axis is the same (poly fit)
ax10.set_ylabel('Exponential Moving Average (EMA)', color='r')
# title(stock)
# Set y axis tick labels to proper graph color
for tl in ax10.get_yticklabels():
	tl.set_color('r')

# Finally include MACD Histogram
# ax3 = ax2.twinx()
# ax3.plot(data_x, macd_histogram, 'g-')
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
