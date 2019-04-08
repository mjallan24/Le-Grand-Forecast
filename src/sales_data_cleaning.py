import pandas as pd
import numpy as np
import datetime



def load_dataframe(file):
    """
    Takes a SQL generated text or csv file and converts it to a pandas dataframe for regression
    """
    df = pd.read_fwf('Le-Grand-Forecast/data/LeGrand2.csv')
    df = df.reset_index()
    df.columns = ['grand_total', 'create_time', 'close_time']

    # Removing the irrelevant rows resulting from read_fwf conversion
    df =df[2:155924]

    # Cleaning data for one timestamp and total
    df = df.reset_index().drop('index', axis=1)
    df['grand_total'] = df['grand_total'].astype(float)
    df = df.drop(labels='close_time', axis=1)
    df['create_time'] = pd.to_datetime(df['create_time'])

    df = df.resample('H', on='create_time').sum()
    df = df.reset_index()

    # Splitting lunch and dinner. Hours based on bimodal nature of hourly sales.
    df['lunch'] = [int(df['create_time'][i].hour >= 10 and df['create_time'][i].hour <= 15)
                    for i in range(len(df))]

    df['dinner'] = [int(df['create_time'][i].hour >= 16 and df['create_time'][i].hour <= 24)
                    for i in range(len(df))]

    df = df.groupby([df['create_time'].dt.date, df['lunch']]).sum()

    df = df.drop(labels=['lunch', 'dinner'], axis=1)

    df = df.reset_index()

    df['lunch_total'] = [int(df['lunch'][i]) * df['grand_total'][i] for i in range(len(df))]

    dinner_total = []
    for i in range(len(df)):
        if df['lunch'][i] == 0:
            dinner_total.append(df['grand_total'][i])
        else:
            dinner_total.append(0)
    df['dinner_total'] = dinner_total

    df.drop(labels='lunch', axis=1)

    df['create_time'] = pd.to_datetime(df['create_time'])

    df_final = df.resample('D', on='create_time').sum()
    df_final.drop(labels='lunch', axis=1, inplace=True)
    df_final = df_final.reset_index()


    # Fixes a specific date where data was inputted incorrectly. 
    # Contacted the owner for the actual values. 
    df_final['create_time'] = pd.to_datetime(df_final['create_time'])
    df_final['grand_total'][1523] = (14280.2)
    df_final['lunch_total'][1523] = (2129.6)
    df_final['dinner_total'][1523] = (12150.6)

    return df_final