import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pyodbc
import pandas as pd
import os
import altair as alt
import time
import sys
sys.path.append(os.path.abspath(r"C:\Users\cyril\Documents\Stocks\TA"))
from AutoSupportAndResistance import *
import talib
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


tickersDF = pd.read_excel(r'C:\Users\cyril\Documents\Stocks\Stocks Dashboard.xlsm', sheet_name='Dividend History')
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

with technicals:
    startDate = st.text_input("Data since: (YYYY-MM-DD Format)", value='2021-01-01')

    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\cyril\\Documents\\Stocks\\DB\\StockHistoricalData.accdb;')
    cursor = conn.cursor()
    cursor.execute('select * from StockHistoricalDB')    
    SQL_Query = pd.read_sql_query(
        '''
        SELECT * FROM StockHistoricalDB 
        WHERE symbol = '%s'
        ORDER BY date''' %ticker, conn
        )
    df = pd.DataFrame(SQL_Query, columns=["ID", "symbol", "date", "open", "high", "low", "close", "volume", "change", "changePercent"])
    df['MA20'] = df.rolling(window=20).mean()['close']
    df['MA50'] = df.rolling(window=50).mean()['close']
    df['MA200'] = df.rolling(window=200).mean()['close']
    df['RSI'] = talib.RSI(df["close"])

    df1 = df[(df['date']>startDate) & (df['date']<'2021-04-04')]

    minClose = float(min(df1['low'].min(),df1['MA200'].min(),df1['MA20'].min()))*0.995
    maxClose = float(max(df1['high'].max(),df1['MA200'].max(),df1['MA20'].max()))*1.005

## LINE CHART

    st.subheader("Close Prices and Linear Regression over Period")

    std_dev = statistics.pstdev(df1['close'])

    chart1 = alt.Chart(df1).mark_line().encode(
            alt.X('date:T', axis=alt.Axis(grid=False, tickSize=0, title="", labels=False)),
            alt.Y('close:Q',axis=alt.Axis(title=""),scale=alt.Scale(domain=[minClose*0.8,maxClose*1.2])),
            color=alt.value(custom_blue)
        )

    chart1_lin_reg = chart1.transform_regression('date','close').mark_line().encode(color=alt.value('red'))

    st.altair_chart(chart1 + chart1_lin_reg,use_container_width=True)
    st.text("Standard Deviation = " + str(round(std_dev,2)))
## CANDLESTICKS CHART

    st.subheader("Moving Averages")
    #annotated_text("Hello ",annotation("world!", "noun", color="#8ef", border="1px dashed red"),)

    open_close_color = alt.condition("datum.open <= datum.close",
                                    alt.value("#06982d"),
                                    alt.value("#ae1325"))
    base = alt.Chart(df1).encode(
        alt.X('date:T',axis=alt.Axis(title="", domain=False, format='%Y-%m-%d', tickSize=0, labelAngle=270, tickCount=df1.shape[0], grid=False)),
        color=open_close_color)

    rule = base.mark_rule().encode(
        alt.Y('low:Q',scale=alt.Scale(domain=[minClose,maxClose])),
        alt.Y2('high:Q'))

    bar = base.mark_bar().encode(
        alt.Y('open:Q'),
        alt.Y2('close:Q'))
    
    MA20_chart = base.mark_line().encode(
        alt.Y('MA20:Q'),
        color=alt.value(custom_blue))

    MA50_chart = base.mark_line().encode(
        alt.Y('MA50:Q'),
        color=alt.value(custom_blue_variant1))

    MA200_chart = base.mark_line().encode(
        alt.Y('MA200:Q',axis=alt.Axis(title="")),
        color=alt.value(custom_blue_variant2))        

    
    st.altair_chart(rule+bar+MA20_chart+MA50_chart+MA200_chart,use_container_width=True)
    #legend:
    annotated_text(annotation("20-Day Period", color=custom_blue, background=background_color1),
            annotation("50-Day Period", color=custom_blue_variant1, background=background_color1),
            annotation("200-Day Period", color=custom_blue_variant2, background=background_color1))
    
## RSI CHART

    st.subheader("RSI")

    chart3 = alt.Chart(df1).mark_line().encode(
            alt.X('date:T',axis=alt.Axis(grid=False, labels=False, tickSize=0, title="")),
            alt.Y('RSI:Q',axis=alt.Axis(title=""),scale=alt.Scale(domain=[0,100])),
            color=alt.value(custom_blue)
        )
    st.altair_chart(chart3, use_container_width=True)

## DIVIDENDS

dividends = st.beta_expander("Dividend History",expanded=True)
with dividends:
    dividendList = yahooTicker.history()['Dividends']>0
    #print(dividendList)

# streamlit run c:\Users\cyril\Documents\Stocks\WebApp\webApp.py

