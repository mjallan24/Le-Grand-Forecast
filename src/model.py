import os
import itertools
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
import datetime
from weather_data_cleaning import load_data
from sales_data_cleaning import load_dataframe

from fbprophet import Prophet

# Load both dataframes and concatenate them
weather = load_data('BFI.txt')
sales = load_dataframe('Le-Grand-Forecast/data/LeGrand2.csv')

df_final = pd.concat([sales, weather], axis=1)

df_lunch = pd.get_dummies(df_final['lunch_cloud'], prefix='lunch')
df_dinner = pd.get_dummies(df_final['dinner_cloud'], prefix='dinner')

df_final = pd.concat([df_final, df_lunch, df_dinner], axis=1)

# Fills nan values with previous day's temperature
df_final['lunch_temp'] = df_final['lunch_temp'].fillna(method='ffill')
df_final['dinner_temp'] = df_final['dinner_temp'].fillna(method='ffill')

# Drop columns that didn't have cloud data
df_final = df_final.drop(labels=['dinner_None', 'lunch_None'], axis=1)

# Facebook Prophet Time Series

df_fb_dinner = df_final.loc[:,['create_time', 'dinner_total']]
df_fb_dinner['create_time'] = pd.to_datetime(df_fb_dinner['create_time'])

df_fb_dinner.columns = ['ds', 'y']
model_dinner = Prophet(seasonality_mode='multiplicative')
model_dinner.add_country_holidays(country_name='US')
model_dinner.fit(df_fb_dinner)

future_mult_dinner = model_dinner.make_future_dataframe(periods=365)
forecast_mult_dinner = model_dinner.predict(future_mult_dinner)
fig = model_dinner.plot(forecast_mult_dinner)
