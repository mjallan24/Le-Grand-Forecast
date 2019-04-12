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

# Lunch Analysis
df_fb_lunch = df_final.loc[:,['create_time', 'dinner_total']]
df_fb_lunch['create_time'] = pd.to_datetime(df_fb_lunch['create_time'])
m = Prophet(seasonality_mode='multiplicative')
m.add_country_holidays(country_name='US')
m.fit(df_fb_lunch)

future_lunch = m.make_future_dataframe(periods=365)
forecast_lunch = m.predict(future_lunch)

# Dinner Analysis
df_fb_dinner = df_final.loc[:,['create_time', 'dinner_total']]
df_fb_dinner['create_time'] = pd.to_datetime(df_fb_dinner['create_time'])

df_fb_dinner.columns = ['ds', 'y']
model_dinner = Prophet(seasonality_mode='multiplicative')
model_dinner.add_country_holidays(country_name='US')
model_dinner.fit(df_fb_dinner)

future_dinner = model_dinner.make_future_dataframe(periods=365)
forecast_mult_dinner = model_dinner.predict(future_dinner)

# Linear Regression Analysis

# Lunch
final_predicted = forecast_lunch.loc[:,['ds','yhat']]
final_predicted = final_predicted[final_predicted['ds'] <= pd.to_datetime('2019-03-29')]

final_actuals = df_final[['create_time','lunch_total']]
y = final_actuals['lunch_total'].values - final_predicted['yhat'].values
X = df_final.loc[:,['lunch_temp','lunch_mostly cloudy', 'lunch_mostly sunny', 'lunch_overcast',
       'lunch_partly sunny', 'lunch_sunny']]

y = pd.DataFrame(y)
y.columns = ['lunch_total']

X = X.reset_index().drop(labels='create_time', axis=1)

lunch_ols_df = pd.concat([X,y], axis=1)
lunch_ols = LinearRegression()
lunch_ols.fit(X,y)
yhat_lunch = lunch_ols.predict(X)

# Dinner

final_predicted_dinner = forecast_mult_dinner.loc[:,['ds','yhat']]
final_predicted_dinner = final_predicted_dinner[final_predicted_dinner['ds'] <= pd.to_datetime('2019-03-29')]

final_actuals_dinner = df_final[['create_time','dinner_total']]
y_dinner = final_actuals_dinner['dinner_total'].values - final_predicted_dinner['yhat'].values
X_dinner = df_final.loc[:,['dinner_temp','dinner_mostly cloudy', 'dinner_mostly sunny', 'dinner_overcast',
       'dinner_partly sunny', 'dinner_sunny']]

y_dinner = pd.DataFrame(y_dinner)
y_dinner.columns = ['dinner_total']

X_dinner = X_dinner.reset_index().drop(labels='create_time', axis=1)

dinner_ols_df = pd.concat([X_dinner,y_dinner], axis=1)

dinner_ols = LinearRegression()
dinner_ols.fit(X_dinner, y_dinner)

yhat_dinner = dinner_ols.predict(X_dinner)