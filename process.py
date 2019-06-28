##########################################
# Author: github.com/uieyao1199
##########################################

import pandas as pd
import multiprocessing as mp
import os
import requests, zipfile, io
import re
import datetime
import string
import time
from datetime import datetime
import pickle
import csv
from time import ctime
from langdetect import detect
import threading
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#full_df=pd.read_csv('AvgTonearg_201503-201603.csv')
#full_df['Date'] = full_df['Date'].apply(lambda x: str(x))
#full_df['Date'] = full_df ['Date'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))

def time_series_graphic(df, col):
    plt.figure(figsize=(10,6))
    plt.plot(df['Date'], df[col])
    plt.xlabel('Date')
    plt.ylabel(col)
    plt.show()

def method_1(df, col):
    meantone = df.loc[:,['Date',col]]
    meantone['avg_diff'] = meantone[col] - meantone[col].mean()

    plt.figure(figsize=(10,6))
    plt.plot(meantone['Date'], meantone['avg_diff'])
    plt.xlabel("Date")
    plt.ylabel(col+'_avgdiff')
    plt.show()

    result = meantone.reindex(meantone.avg_diff.abs().sort_values(ascending=False).index)
    result =result.reset_index(drop=True)
    return result.head(10)

def method_2(df, col):
    meantone = df.loc[:,['Date',col]]
    meantone['t_diff'] = meantone[col].diff()

    plt.figure(figsize=(10,6))
    plt.plot(meantone['Date'], meantone['t_diff'])
    plt.xlabel("Date")
    plt.ylabel(col+"_(t-1)diff")
    plt.show()

    result = meantone.reindex(meantone.t_diff.abs().sort_values(ascending=False).index)
    result = result.reset_index(drop=True)
    return result.head(10)

def method_3(df,col_a1,col_a2,col_b1,col_b2,col_c1,col_c2):
    new_df = df.loc[:,['Date',col_a1,col_a2,col_b1,col_b2,col_c1,col_c2,]]
    new_df.fillna(0, inplace=True)
    new_df['new']=""
    for i in range(len(new_df)):
        a = (new_df.iloc[i,1])*(new_df.iloc[i,2])
        b = (new_df.iloc[i,3])*(new_df.iloc[i,4])
        c = (new_df.iloc[i,5])*(new_df.iloc[i,6])
        NumLan = new_df.iloc[i,[1,3,5]].sum()
        new_df.iloc[i,7]=(a+b+c)/NumLan
    return new_df
