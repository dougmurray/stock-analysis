# main.py
#!/usr/bin/env python27
"""Analysis of stocks using various methods, including ADL, MACD, etc.

   User inputs stock symbol and desired analysis method(s).

   Author:  Douglass Murray
   Date:  2016-03-16
"""
def main_terminal():
    """Runs general Terminal version of script.
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
    print('9 Aerojet Rocketdyne (AJRD)')
    print('10 Johnson & Johnson (JNJ)')
    print('11 MGIC Investment Corp (MTG)')
    print('12 Adamas Pharmaceuticals Inc. (ADMS)')
    print('13 Kraft Heinz (KHC)')
    print('14 ARM Holdings (ARMH)')
    print('15 Wells Fargo (WFC)')
    print('16 Gilead Sciences Inc (GILD)')
    print('17 Mattel Inc (MAT)')

    picked_stock = str(raw_input("Pick stock: "))
    print("you entered", picked_stock)
    return picked_stock
    """
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
    	stock = 'qcom'
    elif picked_stock == 8:
    	stock = 'tsm'
    elif picked_stock == 9:
        stock = 'ajrd'
    elif picked_stock == 10:
        stock = 'jnj'
    elif picked_stock == 11:
        stock = 'mtg'
    elif picked_stock == 12:
        stock = 'adms'
    elif picked_stock == 13:
        stock = 'khc'
    elif picked_stock == 14:
        stock = 'armh'
    elif picked_stock == 15:
        stock = 'wfc'
    elif picked_stock == 16:
        stock = 'gild'
    elif picked_stock == 17:
        stock = 'mat'
    else:
    	stock = ' '
    	print("Please type number representing stock")
    """

if __name__ == '__main__':
    from frontend.runner import *

# TODO: Consider using blessings for fancy text?
