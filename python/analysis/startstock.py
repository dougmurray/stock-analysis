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
def sma(cummulated_data, sma_time_frame):
	"""Calculates the X-day simple moving average, based on:
	   evolving sum(a[:sma_time_frame]) / sma_time_frame

	   Args:
	      cummulated_data: 1D array with close values
	      sma_time_frame: number of days sma average is based on, usually 12, 26, or 9
	   Returns:
	      smas: 1D array with sma values
	"""
	smas = np.array([])
	for i, element in enumerate(cummulated_data):
		if (i + sma_time_frame) >= len(cummulated_data):
			break
		else:
			# sma = sum(sma_time_frame packet) / sma_time_frame 
			sma_element = (sum(cummulated_data[i:sma_time_frame+i]) / sma_time_frame)
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

# Moving Average Convergence/Divergence Oscillator (MACD)
def macd(raw_data):
	"""Calculates MACD, based on:
	   (12-day EMA - 26-day EMA)

	   Args:
	      raw_data: 2D array with [open, high, low, close, volume] per row
	   Returns:
	      macds: 1D array with macds
	"""
	macds = np.array([])
	only_closes = raw_data[:,3]
	ema_12_day = ema(only_closes, 12)
	ema_26_day = ema(only_closes, 26)
	macds = ema_12_day - ema_26_day
	return macds

# Daily Money Flow Multiplier (MFM)
def mfm(mfm_daily_data):
	"""Finds daily money flow multiplier (MFM), represented by:
	   ((close - low) - (high - close)) / (high - low)

	   Args:
	      mfm_daily_data: 2D array with [open, high, low, close, volume] per row
	   Returns:
	      mfms: 1D array with [mfm] values
	"""
	closes = mfm_daily_data[:,3]
	lows = mfm_daily_data[:,2]
	highs = mfm_daily_data[:,1]
	mfms = np.array([])
	for i, data in enumerate(mfm_daily_data):
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
