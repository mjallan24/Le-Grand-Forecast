import pandas as pd
import numpy as np
import datetime



def load_dataframe(file):
    """
    Takes a SQL generated text or csv file and converts it to a pandas dataframe for regression
    """
    df2 = pd.read_fwf('Le-Grand-Forecast/data/LeGrand2.csv')
    df2 = df2.reset_index()
    df2.columns = ['grand_total', 'create_time', 'close_time']

    df2 = df2[2:155924]

    df2 = df2.reset_index().drop('index', axis=1)
    df2['grand_total'] = df2['grand_total'].astype(float)

    df2 = df2.drop(labels='close_time', axis=1)

    df2['create_time'] = pd.to_datetime(df2['create_time'])

    df5 = df2.resample('H', on='create_time').sum()
    df5 = df5.reset_index()

    df5['lunch'] = [int(df5['create_time'][i].hour >= 10 and df5['create_time'][i].hour <= 15)
                    for i in range(len(df5))]

    df5['dinner'] = [int(df5['create_time'][i].hour >= 16 and df5['create_time'][i].hour <= 24)
                    for i in range(len(df5))]

    df5 = df5.groupby([df5['create_time'].dt.date, df5['lunch']]).sum()

    df5 = df5.drop(labels=['lunch', 'dinner'], axis=1)

    df5 = df5.reset_index()

    df5['lunch_total'] = [int(df5['lunch'][i]) * df5['grand_total'][i] for i in range(len(df5))]

    dinner_total = []
    for i in range(len(df5)):
        if df5['lunch'][i] == 0:
            dinner_total.append(df5['grand_total'][i])
        else:
            dinner_total.append(0)
    df5['dinner_total'] = dinner_total

    df5.drop(labels='lunch', axis=1)

    df5['create_time'] = pd.to_datetime(df5['create_time'])

    df_final = df5.resample('D', on='create_time').sum()
    df_final.drop(labels='lunch', axis=1, inplace=True)
    df_final = df_final.reset_index()

    df_final['create_time'] = pd.to_datetime(df_final['create_time'])
    df_final['grand_total'][1523] = (12982*1.1)
    df_final['lunch_total'][1523] = (1936*1.1)
    df_final['dinner_total'][1523] = (11046*1.1)