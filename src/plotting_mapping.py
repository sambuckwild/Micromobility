import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import folium 
from folium.plugins import HeatMap
from scooter_clean import load_data, drop_cols_update_names, cols_to_datetime


def histogram_of_column(df, col, ax, color, title, x_label, x_tick_loc, y_tick_loc, x_low, x_high):
    df[col].hist(color=color, grid=False, bins=30)
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel('Frequency', fontsize=16)
    ax.tick_params(axis='x', which='minor', length=7, width=1)
    ax.tick_params(axis='x', which='major', length=10, width=1, labelsize='medium')
    ax.tick_params(axis='y', which='minor', length=5, width=1)
    ax.tick_params(axis='y', which='major', length=7, width=1, labelsize='medium')
    ax.xaxis.set_minor_locator(MultipleLocator(x_tick_loc))
    ax.yaxis.set_minor_locator(MultipleLocator(y_tick_loc))   
    ax.set_xlim(x_low, x_high)

def bar_chart(df, col, ax, color, label_lst, title, x_label):
    series = df[col].value_counts().sort_index()

    series.plot(kind='bar', color=color)
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel('Frequency', fontsize=16)
    if label_lst == None:
        plt.xticks(rotation=45, fontsize=12)
    else:
        ax.set_xticklabels(labels=label_lst, rotation=45, fontsize=12)

def location_heat_map(df, lat_col, long_col, map_name):
    heat_map = folium.FeatureGroup(name = 'heat_map')
    heat_map.add_child( HeatMap( list(zip(df[lat_col].values,
                                        df[long_col].values)),
                                  name=map_name, max_val=float(60),
                                  min_opacity=0.2, radius=5.5, 
                                  blur=3.5, max_zoom=1))
    return heat_map

def image_file(filepath):
    return plt.savefig(filepath, transparent=False, bbox_inches='tight', format='svg', dpi=1200)

def map_html_file(map_name, filepath):
    return map_name.save(filepath)
    
if __name__ == '__main__':
    # read in week long cleaned dataframe
    scooter_june_pride = load_data('../data/small_scooter.csv')
    scooter_june_pride = drop_cols_update_names(scooter_june_pride, ['Unnamed: 0'])
    scooter_june_pride = cols_to_datetime(scooter_june_pride, ['Start_Time', 'End_Time'])

    '''EDA Histograms'''
    fig, ax = plt.subplots(figsize=(10,6))
    histogram_of_column(scooter_june_pride, 'Trip_Distance', ax, '#DF2C04',
                        'Scooter Trip Distances - Pride Week June 2019', 
                        'Trip Distance, miles', 0.5, 5000, 0, 10)
    image_file('../images/trip_distance_hist.svg')

    '''EDA Bar Plots'''
    weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']
    fig, ax = plt.subplots(figsize=(10,6))
    bar_chart(scooter_june_pride, 'Day_of_Week', ax, '#88D58A', weekdays, 
                'Scooter Trips - Pride Week June 2019', 'Day of the Week')
    image_file('../images/day_of_week_bar.svg')

    '''Origin + Destination Heat Maps'''
    chicago_map = folium.Map(location=[41.862548, -87.749163], zoom_start=11)
    origin_heat_map = location_heat_map(scooter_june_pride, 'Start_Centroid_Latitude', 
                            'Start_Centroid_Longitude', 'Ride Origins')
    origin_heat_map = chicago_map.add_child(origin_heat_map)
    map_html_file(origin_heat_map, '../iamges/origin_heat_map.html')
