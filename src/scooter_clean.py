import pandas as pd 
import numpy as np
from datetime import datetime

def load_data(filepath):
        df = pd.read_csv(filepath)
        return df

def drop_cols_update_names(df, col_lst):
    df.drop(columns=col_lst, inplace=True)
    df.columns = df.columns.str.replace(' ', '_')
    return df

def drop_nans(df):
    return df.dropna(inplace=True)

def cols_to_datetime(df, col_lst):
    for col in col_lst:
        df[col] = pd.to_datetime(df[col])
    return df

def add_weekday_column(df, new_col, date_col):
    df[new_col] = df[date_col].dt.weekday
    return df

def add_hour_column(df, new_col, date_col):
    df[new_col] = df[date_col].dt.hour
    return df

def change_col_units(df, col, divisor):
    df[col] = df[col].apply(lambda x: x/divisor)
    return df

def filter_out_bad_data(df, col_lst, threshold_lst):
    for col, thresh in zip(col_lst, threshold_lst):
        if thresh < 20:
            df = df[df[col] > thresh]
        else:
            df = df[df[col] < thresh]
    df.reset_index(drop=True)
    return df

def clean_dataframe(df, drop_col_lst, date_col_lst, day_col, hour_col, date_col, 
                        unit_col_1, unit_col_2, div_1, div_2, filter_col_lst, thresh_lst):

    df = drop_cols_update_names(df, drop_col_lst)
    drop_nans(df)
    df = cols_to_datetime(df, date_col_lst)
    df = add_weekday_column(df, day_col, date_col)
    df = add_hour_column(df, hour_col, date_col) 
    df = change_col_units(df, unit_col_1, div_1)
    df = change_col_units(df, unit_col_2, div_2)
    df = filter_out_bad_data(df, filter_col_lst, thresh_lst)
    return df.reset_index(drop=True)

def data_snapshot(df, col, low_end, high_end):
    df = df[df[col] > low_end]
    df = df[df[col] <= high_end]
    return df.reset_index(drop=True)

def save_dataframe_to_csv(df, filepath):
    return df.to_csv(filepath)


if __name__ == '__main__':
    # scooter = load_data('../data/2019_Scooter_pilot.csv')
    scooter = clean_dataframe(df=scooter, 
                            drop_col_lst=['Start Census Tract', 'End Census Tract',
                            'Start Community Area Number', 'End Community Area Number', 
                            'Start Community Area Name', 'End Community Area Name', 
                            'Start Centroid Location', 'End Centroid Location'],
                            date_col_lst=['Start_Time', 'End_Time'],
                            day_col='Day_of_Week',
                            hour_col='Time_of_Day',
                            date_col='Start_Time',
                            unit_col_1='Trip_Distance',
                            div_1=1609,
                            unit_col_2='Trip_Duration',
                            div_2=60,
                            filter_col_lst=['Trip_Distance', 'Trip_Duration', 'Trip_Duration'],
                            thresh_lst=[25, 2, 400])
                           
    '''make week long dataset'''
    small_scooter = data_snapshot(scooter, 'Start_Time', '2019-06-21', '2019-06-30')
    save_dataframe_to_csv(small_scooter, '../data/small_scooter.csv')
    
    '''clean full dataset - six features'''
    clean_scooter = load_data('../data/full_clean_scooter.csv')
    clean_scooter.drop(columns=['Unnamed: 0', 'Trip_ID', 'Start_Time', 'End_Time', 
                        'Accuracy', 'End_Centroid_Latitude',
                            'End_Centroid_Longitude'], inplace=True)
    
	
    
    
    
    
    