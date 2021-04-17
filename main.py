import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
#import pyodbc
import pandas as pd
import os
import altair as alt
#import time
import sys
sys.path.append(os.path.abspath(r"C:\Users\cyril\Documents\Stocks\TA"))
from AutoSupportAndResistance import *
#import talib
from annotated_text import annotated_text, annotation
import statistics
import numpy as np
from sklearn.linear_model import LinearRegression

#### To-Do List:
# DONE - add linear regression on CHART 1
# add ecart type 1+2 on CHART 1
# add financial statements of the last x years in Fundamental Tab - add ebit, margin etc.
# -> TO, EBITDA, Revenue, P/E (=Current Price / EPS), P/S, Market Cap, Last Price, Payout, last 5 dividends, bookValue
# add news from Reuters 
# take currency into account ex: "Total Revenue & Currency"

######## Colors:
custom_blue = "#33BCF6"
custom_blue_variant1 = "#78CFF8"
custom_blue_variant2 = "#A9E1FB"
custom_blue_variant3 = "#D5F2FF"
custom_blue_variant4 = "#9CB5C1"
custom_blue_variant5 = "#677C86"
background_color1 = "#262730"
background_color2 = "#36474F"
text_color = "#FFFFFF"
########


####### STYLING
# current = shades of blue
# possible alternative:
# green for best = 06982d red for worth = #ae1325 ??

st.markdown("""
<style>
.custom_blue {
    color: %s;
    font-size: 15px;
}
</style>
"""%custom_blue, unsafe_allow_html=True)

st.markdown("""
<style>
.custom_blue_variant1 {
    color: %s;
    font-size: 15px;
}
</style>
"""%custom_blue_variant1, unsafe_allow_html=True)

st.markdown("""
<style>
.custom_blue_variant2 {
    color: %s;
    font-size: 15px;
}
</style>
"""%custom_blue_variant2, unsafe_allow_html=True)

st.markdown("""
<style>
.custom_blue_variant3 {
    color: %s;
    font-size: 15px;
}
</style>
"""%custom_blue_variant3, unsafe_allow_html=True)

st.markdown("""
<style>
.custom_blue_variant4 {
    color: %s;
    font-size: 15px;
}
</style>
"""%custom_blue_variant4, unsafe_allow_html=True)

st.markdown("""
<style>
.custom_blue_variant5 {
    color: %s;
    font-size: 15px;
}
</style>
"""%custom_blue_variant5, unsafe_allow_html=True)

text_styles = ["custom_blue","custom_blue_variant1","custom_blue_variant2",
                "custom_blue_variant3","custom_blue_variant4","custom_blue_variant5"]

#st.markdown('<p class="custom_blue">Hello World !!</p>', unsafe_allow_html=True)
#######

def highlight_max(data, color=custom_blue):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr = 'background-color: {}'.format(color)
    #remove % and cast to float
    data = data.replace('%','', regex=True).astype(float)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)

def writeData(data,name,dataType="value"): #name="Gross Profit", data=financials
    st.subheader(name)
    col1,col2,col3,col4 = st.beta_columns([1,1,1,1])
    cols = [col1,col2,col3,col4]
    sorted_column = data.loc[name].sort_values(ascending=False) ###
    for i in range(4):
        if dataType=="percent":
            position = sorted_column.index.get_loc(data.columns[i])
            data.loc[name][i] = str(round(data.loc[name][i]*100,1))+"%"
            with cols[i]:
                st.text(data.columns[i].year)
                #st.text(data.loc[name][i])
                #use markdown for color:
                st.markdown('<p class="%s">%s</p>'%(text_styles[position],data.loc[name][i]),unsafe_allow_html=True)
        else:
            position = sorted_column.index.get_loc(data.columns[i])
            if round(data.loc[name][i]/1000000000,2) < 1:
                data.loc[name][i] = str(round(data.loc[name][i]/1000000,2))+" M€"
            else:
                data.loc[name][i] = str(round(data.loc[name][i]/1000000000,2))+" B€"
            with cols[i]:
                st.text(data.columns[i].year)
                #st.text(data.loc[name][i])
                #use markdown for color:
                st.markdown('<p class="%s">%s</p>'%(text_styles[position],data.loc[name][i]),unsafe_allow_html=True)


tickersDF = pd.read_excel('Stocks Dashboard.xlsm', sheet_name='Dividend History')
tickers = []

tickers = tickersDF['Symbol'].tolist()
tickers = sorted(tickers)
ticker = st.sidebar.selectbox("Selected Symbol:", tickers)
# for comparison page:
# ticker = st.sidebar.multiselect("Symbols", tickers)
# will require WHERE symbol IN list in SQL request

yahooTicker = yf.Ticker(ticker)
info = yahooTicker.info
financials = yahooTicker.financials#.transpose()

financials.loc['Profit Margin'] = financials.loc['Net Income'] / financials.loc['Total Revenue']

financials.columns = financials.columns.date

financials = financials#.transpose()
#financials.loc["Ebit"][0], financials.columns[0]

#financials['Profit Margin'] = financials['Net Income'] / financials['Total Revenue']
try:
    longBusinessSummary = info['longBusinessSummary']
except:
    pass
try:
    website = info['website']
except:
    pass
try:
    logo_url = info['logo_url']
except:
    pass
try:
    currency = info['currency']
except:
    currency = "EUR"


# TITLE
col1,mid,col2 = st.beta_columns([4,1,15])
with col2:
    st.title(info['longName'])
with col1:
    try:
        st.image(logo_url,width=100)
    except:
        pass

# GENERAL INFO

generalInfo = st.beta_expander("General Information")
with generalInfo:
    try:
        st.write(longBusinessSummary)
    except:
        pass
    try:
        st.write(website)
    except:
        pass

fundamentals = st.beta_expander("Fundamental Analysis",expanded=True)
with fundamentals:
    writeData(financials,"Total Revenue")
    writeData(financials,"Gross Profit")
    writeData(financials,"Net Income")
    writeData(financials,"Ebit")
    # must add optional argument to writeData to select %
    # print(financials.loc["Profit Margin"])
    writeData(financials,"Profit Margin",dataType="percent") # = net income / total revenue
    
    #st.dataframe(financials.style.apply(highlight_max))

technicals = st.beta_expander("Technical Analysis",expanded=True)



# streamlit run c:\Users\cyril\Documents\Stocks\WebApp\webApp.py

