import pandas as pd
import numpy as np
import datetime

def load_data(file):
    df = pd.read_csv(file)
    df = find_nan_columns(df)

    df['valid'] = pd.to_datetime(df['valid'])

    clouds = [to_category(df['metar'][i], df['valid'][i].hour) for i in range(len(df))]

    df['cloud_cover'] = clouds

    df = df.rename(columns = {'tmpf': 'temp', 'p01i': 'precip', 'dwpf': 'dew_temp', 'relh': 'humidity'})

    lunch_temp = []
    dates_lunch = []
    for i in range(len(df)):
        
        # Checks for temp at hour 10, if there is a temp value, and if the date is already in the column
        if df['valid'][i].hour == 10 and str(df['valid'][i].date()) not in dates_lunch and not np.isnan(df['temp'][i]):
            lunch_temp.append(((df['temp'][i]),str(df['valid'][i].date())))
            dates_lunch.append(str(df['valid'][i].date()))

    dinner_temp = []
    dates_dinner = []
    for i in range(len(df)):
        
        # Checks for temp at hour 16, if there is a temp value, and if the date is already in the column
        if df['valid'][i].hour == 16 and str(df['valid'][i].date()) not in dates_dinner and not np.isnan(df['temp'][i]):
            dinner_temp.append(((df['temp'][i]),str(df['valid'][i].date())))
            dates_dinner.append(str(df['valid'][i].date()))

    lunch_cat = []
    dates_lunch = []
    for i in range(len(df)):
        
        # Checks for cloud cover at hour 10, if there is a value, and if the date is already in the column
        if df['valid'][i].hour == 10 and str(df['valid'][i].date()) not in dates_lunch and (df['cloud_cover'][i]):
            lunch_cat.append(((df['cloud_cover'][i]),str(df['valid'][i].date())))
            dates_lunch.append(str(df['valid'][i].date()))

    dinner_cat = []
    dates_dinner = []
    for i in range(len(df)):
        
        # Checks for cloud cover at hour 16, if there is a value, and if the date is already in the column
        if df['valid'][i].hour == 16 and str(df['valid'][i].date()) not in dates_dinner and (df['cloud_cover'][i]):
            dinner_cat.append(((df['cloud_cover'][i]),str(df['valid'][i].date())))
            dates_dinner.append(str(df['valid'][i].date()))


    lunch_temp = pd.DataFrame(lunch_temp)
    lunch_temp.columns = ['lunch_temp', 'create_time']

    dinner_temp = pd.DataFrame(dinner_temp)
    dinner_temp.columns = ['dinner_temp', 'create_time']

    lunch_cat = pd.DataFrame(dinner_cat)
    lunch_cat.columns = ['lunch_cloud', 'create_time']

    dinner_cat = pd.DataFrame(dinner_cat)
    dinner_cat.columns = ['dinner_cloud', 'create_time']

    lunch_temp['create_time'] = pd.to_datetime(lunch_temp['create_time'])
    dinner_temp['create_time'] = pd.to_datetime(dinner_temp['create_time'])

    lunch_cat['create_time'] = pd.to_datetime(lunch_cat['create_time'])
    dinner_cat['create_time'] = pd.to_datetime(dinner_cat['create_time'])

    # Setting indices to datetime for concatanation prep

    lunch_temp = lunch_temp.set_index('create_time')
    dinner_temp = dinner_temp.set_index('create_time')

    lunch_cat = lunch_cat.set_index('create_time')
    dinner_cat = dinner_cat.set_index('create_time')

    new_df = pd.concat([lunch_temp, dinner_temp, lunch_cat, dinner_cat], axis=1)
    return new_df

def to_category(raw_metar, hour):

    """
    Converts raw metar data into categories for the level of cloud cover.

    Inputs: (string)    raw metar data
            (int)       hour pulled from timestamp object
    
    Output: (string)    categorical term for cloud cover
    """
    if not raw_metar or type(raw_metar) != str:
        return 'None'
    else:

        if any(elem in raw_metar for elem in ["SKC", "CLR"]):
            return "sunny"
        elif "FEW" in raw_metar:
            return "mostly sunny"
        elif "SCT" in raw_metar:
            return "partly sunny"
        elif "BKN" in raw_metar:
            return "mostly cloudy"
        elif "OVC" in raw_metar:
            return "overcast"
        else:
            return 'None'

def find_nan_columns(df):
    """
    Finds and drops columns with over 90% NaN values
    
    Input: pandas DataFrame
    
    Output: pandas DataFrame
    """
    cols_to_drop = []
    for col in df.columns:
        if (df[col].isna().sum() > (df.shape[0]*.9)):
            cols_to_drop.append(col)
    df.drop(labels=cols_to_drop, axis=1, inplace=True)
    return df