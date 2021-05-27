import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.dates as mdates
import plotly as py
import plotly.graph_objects as go

# Real World Finance dataset:
api_key = '40U5ZR97VALZHOQE'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='IBM', interval='1min', outputsize='full')
print(data)

# Retrieving datasets from Kaggle and importing into Pandas
AFL_bank = pd.read_csv("AFL.csv")
print(AFL_bank.head())
print(AFL_bank.info())
print(AFL_bank.describe)
print(AFL_bank.columns)
print(AFL_bank.values)
print(AFL_bank.info())

JPMorgan = pd.read_csv("JPM.csv")
print(JPMorgan.head())

US_Historical = pd.read_csv("dataset_summary (1).csv")
print(US_Historical.head)

# Analyzing Data
# Volatility of IBM Stock
close_data = data['4. close']
percentage_change = close_data.pct_change()

print(percentage_change)

last_change = percentage_change[-1]

if abs(last_change) > 0.0004:
    print("IBM Alert:" + 'last_change')
# Sorting AFL Bank by descending Volume
AFL_bank_vol = AFL_bank.sort_values("Volume", ascending=False)
print(AFL_bank_vol.head())

# Sorting AFL Bank by date, then descending Close Values
AFL_bank_date_close = AFL_bank.sort_values(["Date", "Close"], ascending=[True, False])
print(AFL_bank_date_close.head())

# Selecting High and Low Columns from AFL_bank
AFL_bank_high_low = AFL_bank[["High", "Low"]]
print(AFL_bank_high_low.head())

# Filtering for rows where Open Value is less than 10 in AFL_bank
AFL_bank_vol_open = AFL_bank[(AFL_bank["Open"] < 10)]
print(AFL_bank_vol_open)

# Indexing AFL Bank by Date
AFL_bank_ind = AFL_bank.set_index("Date")
print(AFL_bank_ind)

# Using Slicing to get columns 3 to 4 in JPMorgan
print(JPMorgan.iloc[0:, 2:4])

# Adding a Column = Open minus Close for JPMorgan
JPMorgan["JPMorgan_minus"] = JPMorgan["Open"] - JPMorgan["Close"]
print(JPMorgan)

# Printing the median of Adj Close for JPMorgan
print(JPMorgan["Adj Close"].median())

# Grouping JPMorgan by Date
JPMorgan_by_date = JPMorgan.groupby("Date")["High"].agg([min, max, sum])
print(JPMorgan_by_date)

# Counting missing values in each column
missing_values_count = US_Historical.isnull().sum()
print(missing_values_count[0:5])

# Dropping columns where data is missing
dropcolumns = US_Historical.dropna(axis=1)
print(US_Historical.shape, dropcolumns.shape)

# Filling all missing values with 0
cleaned_data = US_Historical.fillna(0)

# Loops
for columns in AFL_bank:
    print(columns)
    break

# Using a while loop to save data for IBM into excel
# (Commented to not interfere with the script-takes too long to run)
#i = 1
#while i==1:
#    data, meta_data = ts.get_intraday(symbol='IBM', interval='1min', outputsize='full')
#    data.to_excel("output.xlsx")
#    time.sleep(60)

# Merging tables AFL_bank and JPMorgan with a inner join
JPMorgan_Date = pd.to_datetime(JPMorgan.Date)
AFL_bank_Date = pd.to_datetime(AFL_bank.Date)
JPM_AFL = AFL_bank.merge(JPMorgan, on='Date')
print(JPM_AFL.head(4))

# Creating a list from AFL_bank
with open('AFL.csv', 'r') as f:
    AFL_list = list(csv.reader(f, delimiter=':'))
print(AFL_list[:3])

# List into Numpy Arrays
AFL_array = np.array(AFL_list)
print(type(AFL_array))
print(AFL_array.shape)

# Transposing AFL_array
AFL_array_transposed = np.transpose(AFL_array)
print(AFL_array_transposed)
print(AFL_array_transposed.size)
print(AFL_array_transposed.shape)

# Subset 3rd row from AFL_array transposed
AFL_array_sub = AFL_array_transposed[:, 3]
print(AFL_array_sub)

# Plots
# API 'IBM' RSA & SMA graph
period = 120

ti = TechIndicators(key=api_key, output_format='pandas')

data_ti, meta_data_ti = ti.get_rsi(symbol='IBM', interval='1min',
                                   time_period=period, series_type='close')

data_sma, meta_data_Sma = ti.get_sma(symbol='IBM', interval='1min',
                                     time_period=period, series_type='close')

df1 = data_sma.iloc[1::]
df2 = data_ti
df1.index = df2.index

fig, ax = plt.subplots()
ax.plot(df1, 'b-')
ax2 = ax.twinx()
ax2.plot(df2, 'r.')
plt.title("SMA & RSI graph")
plt.show()

# JPMorgan Daily Closing Price
JPM = pd.read_csv('JPM.csv', header=0, index_col='Date', parse_dates=True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.grid(True)
plt.xticks(rotation=90)
plt.plot(JPM.index, JPM['Adj Close'])
plt.title("Daily Closing Prices")
plt.show()

# AFL Historical stock prices
AFL = AFL_bank.iloc[::-1]
AFL['Date'] = pd.to_datetime(AFL['Date'])
AFL['20wma'] = AFL['Close'].rolling(window = 140).mean()
fig2 = go.Figure(data = [go.Candlestick(x=AFL['Date'],
                        open=AFL['Open'], high= AFL['High'],
                        low=AFL['Low'], close=AFL['Close'])])
fig2.add_trace(
    go.Scatter(
        x=AFL['Date'],
        y=AFL['20wma'],
        line=dict(color="#e0e0e0"),
        name="20-week"
    ))

fig2.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")
fig2.update_layout(yaxis_title="AFL price", xaxis_title="Date")
fig2.update_yaxes(type="log")
fig2.show()


