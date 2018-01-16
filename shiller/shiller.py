#!/usr/bin/env python
"""

Import Robert Shiller's P,E,CPI,Interest rate data.

"""

import os
# import urllib2
from urllib.request import urlopen

import pandas as pd
import numpy as np


mod_dir = os.path.dirname(__file__)
csv_file = os.path.join(mod_dir, 'shiller.csv')


if not os.path.exists(csv_file):
    xls_url = 'http://www.econ.yale.edu/~shiller/data/chapt26.xlsx'
    # url = urllib2.urlopen(xls_url)
    url = urlopen(xls_url)

    xls = pd.ExcelFile(url)
    df = xls.parse('Data', skiprows=[0,1,3,4,5,6,7],
                   skip_footer=5, index_col=0)

    df.to_csv(csv_file)

else:
    df = pd.read_csv(csv_file, index_col=0)

df['Interest_rates'] = df['RLONG'] / 100. # convert from percent to fraction
stock_price = df['P']
stock_div   = df['D']
# Stock market rate of return
df['stock_increase'] = (stock_price.diff() + stock_div).iloc[1:-1]
df['stock_returns'] = df['stock_increase'] / stock_price.iloc[1:-1]
df['inflation'] = df['CPI'].diff() / df['CPI']

# drop rows with nan
df.dropna(axis=0,how='any',inplace=True)

## Computing annualized changes

def inflation():
    # Inflation rate
    return df['inflation'].iloc[1:-1]

def interest_rates():
    return df['Interest_rates']

def stock_returns():
    return df['stock_returns']


dates = df['CPI'].index

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib import rcParams

    rcParams['figure.figsize'] = [7.,3.5]

    plt.figure()

    plt.plot(dates, 100*stock_returns, label='stock returns', 
             lw=0.7)

    plt.plot(dates, 100*inflation(), label='inflation', ls='--')

    plt.plot(dates, 100*interest_rates, label='long term interest', ls=':')

    plt.ylabel('Annualized Rate (%)')
    plt.legend(loc='lower left', fontsize='small')

    plt.savefig('historical-trends.pdf')
