import pandas as pd
import numpy as np
import datetime



def load_dataframe(file):
    """
    Takes a SQL generated text or csv file and converts it to a pandas dataframe for regression
    """
    df = pd.read_fwf('file')
    df = df.reset_index()
    df.columns = ['grand_total', 'create_time', 'close_time']
    df = df[2:155924]

    df = df.reset_index().drop('index', axis=1)
    df['grand_total'] = df['grand_total'].astype(float)
    df['create_time'] = pd.to_datetime(df['create_time'])

    df = df.drop(labels='close_time', axis=1) 

    return df


