# main.py
#!/usr/bin/env python27
from frontend.runner import *
# from analysis import startstock
"""Analysis of stocks using various methods, including ADL, MACD, etc.

   User inputs stock symbol and desired analysis method(s).  

   Author:  Douglass Murray
   Date:  2016-03-16
"""

print("Welcome to Stock Analysis Program")
print("Available stocks are: ")
print('1 Microchip (MCHP)')
print('2 Hershey (HSY)')
print('3 Micro (MU)')
print('4 Nike (NKE)')
print('5 Intel (INTC)')
print('6 JD.com (JD)')
print('7 Qualcomm (QCOM)')
print('8 Taiwan Semiconductor (TSM)')

picked_stock = int(raw_input("Pick stock: "))
print("you entered", picked_stock)

if picked_stock == 1:
	stock = 'mchp'
elif picked_stock == 2:
	stock = 'hsy'
elif picked_stock == 3:
	stock = 'mu'
elif picked_stock == 4:
	stock = 'nke'
elif picked_stock == 5:
	stock = 'intc'
elif picked_stock == 6:
	stock = 'jd'
elif picked_stock == 7:
	stock = 'gcom'
elif picked_stock == 8:
	stock = 'tsm'
else:
	stock = ' '
	print("Please type number representing stock")

# Consider using blessings for fancy text?