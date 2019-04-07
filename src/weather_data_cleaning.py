import pandas as pd
import numpy as np
import datetime

def load_data(file):
    df = pd.read_csv('file')
    df = find_nan_columns(df)

    # Rename relevant columns to more readable names
    df.rename(columns = {'tmpf': 'temp', 'p01i': 'precip', 'dwpf': 'dew_temp', 'relh': 'humidity'})

    df['clouds'] = [to_category(df['metar'][i], df['valid'][i].hour) for i in range(len(df))]


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



def to_category(raw_metar, hour):

    """
    Converts raw metar data into categories for the level of cloud cover.

    Inputs: (string)    raw metar data
            (int)       hour pulled from timestamp object
    
    Output: (string)    categorical term for cloud cover
    """
    if not raw_metar or type(raw_metar) != str:
        return np.nan
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
            return np.nan