## Calculate Support and Resistance of a Stock over a Period
## entries: ticker name, period
## returns: supports and resistance, entually prints it

import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
import pandas_datareader as web
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression
import yfinance as yf
from sklearn.metrics import r2_score


def pythag(pt1, pt2):
    a_sq = (pt2[0] - pt1[0]) ** 2
    b_sq = (pt2[1] - pt1[1]) ** 2
    return sqrt(a_sq + b_sq)

def local_min_max(pts):
    local_min = []
    local_max = []
    prev_pts = [(0, pts[0]), (1, pts[1])]
    for i in range(1, len(pts) - 1):
        append_to = ''
        if pts[i-1] > pts[i] < pts[i+1]:
            append_to = 'min'
        elif pts[i-1] < pts[i] > pts[i+1]:
            append_to = 'max'
        if append_to:
            if local_min or local_max:
                prev_distance = pythag(prev_pts[0], prev_pts[1]) * 0.5
                curr_distance = pythag(prev_pts[1], (i, pts[i]))
                if curr_distance >= prev_distance:
                    prev_pts[0] = prev_pts[1]
                    prev_pts[1] = (i, pts[i])
                    if append_to == 'min':
                        local_min.append((i, pts[i]))
                    else:
                        local_max.append((i, pts[i]))
            else:
                prev_pts[0] = prev_pts[1]
                prev_pts[1] = (i, pts[i])
                if append_to == 'min':
                    local_min.append((i, pts[i]))
                else:
                    local_max.append((i, pts[i]))
    return local_min, local_max

# symbol = 'MC.PA'
# df = web.DataReader(symbol, 'yahoo', '2010-01-01', '2019-04-01')
# series = df['Close']
# series.index = np.arange(series.shape[0])

# month_diff = series.shape[0] // 30 # Integer divide the number of prices we have by 30
# if month_diff == 0: # We want a value greater than 0
#     month_diff = 1
# smooth = int(2 * month_diff + 3) # Simple algo to determine smoothness
# pts = savgol_filter(series, smooth, 3) # Get the smoothened price data

# x = series.index
# y = series

# model = np.polyfit(x, y, 1)

# predict = np.poly1d(model)
# from sklearn.metrics import r2_score
# r2_score(y, predict(x))
# x_lin_reg = range(0, 3000)
# y_lin_reg = predict(x_lin_reg)
#plt.scatter(x, y)

def findLinearReg(df):
    series = df['Close']
    series.index = np.arange(series.shape[0])
    month_diff = series.shape[0] // 30 # Integer divide the number of prices we have by 30
    if month_diff == 0: # We want a value greater than 0
        month_diff = 1
    smooth = int(2 * month_diff + 3) # Simple algo to determine smoothness
    pts = savgol_filter(series, smooth, 3) # Get the smoothened price data
    x = series.index
    y = series
    model = np.polyfit(x, y, 1)
    predict = np.poly1d(model)
    r2_score(y, predict(x))
    x_lin_reg = range(0, 3000)
    y_lin_reg = predict(x_lin_reg)
    return x_lin_reg, y_lin_reg

# x_lin_reg,y_lin_reg=findLinearReg(df)
# print(x_lin_reg,y_lin_reg)
# plt.plot(x_lin_reg, y_lin_reg, c = 'r')
# plt.show()
