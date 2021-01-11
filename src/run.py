import pandas as pd 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import folium 
from folium.plugins import HeatMap
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import silhouette_score

from scooter_clean import *
from plotting_mapping import *
from model import *


if __name__ == '__main__':
    # '''read in week long cleaned dataframe'''
    scooter_june_pride = load_data('../data/small_scooter.csv')
    scooter_june_pride = drop_cols_update_names(scooter_june_pride, ['Unnamed: 0'])
    scooter_june_pride = cols_to_datetime(scooter_june_pride, ['Start_Time', 'End_Time'])
    
    '''clean full dataset - six features'''
    clean_scooter = load_data('../data/full_clean_scooter.csv')
    clean_scooter.drop(columns=['Unnamed: 0', 'Trip_ID', 'Start_Time', 'End_Time', 
                        'Accuracy', 'End_Centroid_Latitude',
                            'End_Centroid_Longitude'], inplace=True)
    #kmeans model with full dataset and five clusters
    kmeans_fulldf = kmeans_model(clean_scooter, n_clust=5)
    print('cluster centers:{}'.format(kmeans_fulldf.cluster_centers_))

    #heat map with cluster center geo-coordinates mapped
    cluster_center_df = get_cluster_geo_df(kmeans_fulldf, n_clust=5)
    chicago_map_fulldf = folium.Map(location=[41.88955765, -87.71819668], zoom_start=11)
    for i, row in cluster_center_df.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                    popup=row['name'], color='b').add_to(chicago_map_fulldf)
    heat_map_fulldf = folium.FeatureGroup(name = 'heat_map')
    heat_map_fulldf.add_child( HeatMap( list(zip(clean_scooter['Start_Centroid_Latitude'].values,
                                        clean_scooter['Start_Centroid_Longitude'].values)),
                                name='Origins',
                                max_val=float(60),
                    min_opacity=0.2,
                    radius=5.5, blur=3.5, 
                    max_zoom=1, 
                    ))
    chicago_map_fulldf.add_child(heat_map_fulldf)
    map_html_file(heat_map_fulldf, 'full_df_cluster_center_heatmap.html')
    chicago_map_fulldf

    '''EDA Histograms'''
    fig, ax = plt.subplots(figsize=(10,6))
    histogram_of_column(scooter_june_pride, 'Trip_Distance', ax, '#DF2C04',
                        'Scooter Trip Distances - Pride Week June 2019', 
                        'Trip Distance, miles', 0.5, 5000, 0, 10)
#     image_file('../images/trip_distance_hist.svg')

    fig, ax = plt.subplots(figsize=(10,6))
    histogram_of_column(scooter_june_pride, 'Trip_Duration', ax, '#FBAF00',
                        'Scooter Trip Durations - Pride Week June 2019', 
                        'Trip Length, minutes', 10, 5000, 0, 150 )
#     image_file('../images/trip_duration_hist.svg')

    '''EDA Bar Plots'''
    weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday', 'Sunday']
    fig, ax = plt.subplots(figsize=(10,6))
    bar_chart(scooter_june_pride, 'Day_of_Week', ax, '#88D58A', weekdays, 
                'Scooter Trips - Pride Week June 2019', 'Day of the Week')
#     image_file('../images/day_of_week_bar.svg')

    hours=['Midnight', '1am', '2am','5am', '6am', '7am', '8am', '9am', '10am', '11am', '12pm',
            '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm',]
    fig, ax = plt.subplots(figsize=(10,6))
    bar_chart(scooter_june_pride, 'Time_of_Day', ax, '#0DD4FC', hours,
                'Scooter Trips - Pride Week June 2019', 'Time of Day, Hour')
#     image_file('../images/hour_of_day_bar.svg')

    '''Origin + Destination Heat Maps'''
    chi_map1= folium.Map(location=[41.862548, -87.749163], zoom_start=11)
    origin_heat_map = location_heat_map(scooter_june_pride, 'Start_Centroid_Latitude', 
                            'Start_Centroid_Longitude', 'Ride Origins')
    origin_heat_map = chi_map1.add_child(origin_heat_map)
#     map_html_file(origin_heat_map, '../images/origin_heat_map.html')

    chi_map2= folium.Map(location=[41.862548, -87.749163], zoom_start=11)
    dest_heat_map = location_heat_map(scooter_june_pride, 'End_Centroid_Latitude', 
                            'End_Centroid_Longitude', 'Ride Destinations')
    dest_heat_map = chi_map2.add_child(dest_heat_map)
#     map_html_file(dest_heat_map, '../images/dest_heat_map.html')

    '''K-Means Modeling'''
    origin_array = coord_location_array(scooter_june_pride, 
                      'Start_Centroid_Latitude', 'Start_Centroid_Longitude')
    destination_array = coord_location_array(scooter_june_pride,
                            'End_Centroid_Latitude', 'End_Centroid_Longitude')
    origin_kmeans = kmeans_model(origin_array)
    print('cluster centers:{}'.format(origin_kmeans.cluster_centers_)) 
    dest_kmeans = kmeans_model(destination_array)
    print('cluster centers:{}'.format(dest_kmeans.cluster_centers_))

    origin_sil_scores = [calc_silhouette_score(i, origin_array) for i in range(2,10)]
    dest_sil_scores = [calc_silhouette_score(i, destination_array) for i in range(2,10)]

    fig, ax = plt.subplots(figsize=(10,6))
    silhouette_plot(ax, origin_sil_scores, 'b', 'Ride Origins', 
                        'Silhouette Score vs K - Scooter Rides')
    silhouette_plot(ax, dest_sil_scores, 'm', 'Ride Destinations', 
                        'Silhouette Score vs K - Scooter Rides')
#     image_file('../images/origin_dest_sil_plot.svg')

    #run the models again with 8 clusters for origin and 5 for destination
    origin_kmeans = kmeans_model(origin_array, n_clust=8)
    origin_clusters = origin_kmeans.cluster_centers_
    dest_kmeans = kmeans_model(destination_array, n_clust=5)
    dest_clusters = dest_kmeans.cluster_centers_
    
    fig, ax = plt.subplots(figsize=(10,6))
    kmeans_scatter_plot(ax, origin_clusters, 'b', 75, 'Cluster Centers', 
                    'Ride Origins & K-Means Model Cluster Centers')
    kmeans_scatter_plot(ax, origin_array, 'grey', 8, 'Rider Origins', 
                    'Ride Origins & K-Means Model Cluster Centers')
    # image_file('../images/kmeans_origin_scatter.svg')

    fig, ax = plt.subplots(figsize=(10,6))
    kmeans_scatter_plot(ax, dest_clusters, 'm', 75, 'Cluster Centers', 
                    'Ride Destinations & K-Means Model Cluster Centers')
    kmeans_scatter_plot(ax, destination_array, 'grey', 8, 'Rider Destinations', 
                    'Ride Destinations & K-Means Model Cluster Centers')
    # image_file('../images/kmeans_dest_scatter.svg')

   #  plot clusters on top of heat maps'''
    origin_clust_df = cluster_center_df(origin_clusters, ['lat', 'lon'])
    dest_clust_df = cluster_center_df(dest_clusters, ['lat', 'lon'])

    chi_map3 = folium.Map(location=[41.88955765, -87.71819668], zoom_start=12)
    for i, row in origin_clust_df.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        popup=row['name']).add_to(chi_map3)
    origin_heat_map2 = location_heat_map(scooter_june_pride, 'Start_Centroid_Latitude', 
                            'Start_Centroid_Longitude', 'Ride Origins')
    origin_heat_map2 = chi_map3.add_child(origin_heat_map2)
#     map_html_file(origin_heat_map2, '../images/origin_cluster_heat_map.html')

    chi_map4 = folium.Map(location=[41.88955765, -87.71819668], zoom_start=12)
    for i, row in dest_clust_df.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        popup=row['name']).add_to(chi_map4)
    dest_heat_map2 = location_heat_map(scooter_june_pride, 'End_Centroid_Latitude', 
                            'End_Centroid_Longitude', 'Ride Destinations')
    dest_heat_map2 = chi_map4.add_child(dest_heat_map2)
#     map_html_file(dest_heat_map2, '../images/origin_cluster_heat_map.html')

    '''hierarchical clustering model'''                                          
    origin_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                origin_array)
    dest_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                destination_array)
    fig, ax = plt.subplots(figsize=(24, 12))
    dendrogram_plot(origin_hier_clust, ax, 6, 'level', 0.076,
                        'Ride Origin Dendrogram with 7 Clusters')
#     image_file('../images/origin_dendrogram.svg')

    fig, ax = plt.subplots(figsize=(24, 12))
    dendrogram_plot(dest_hier_clust, ax, 6, 'level', 0.12,
                        'Ride Destination Dendrogram wtih 5 Clusters')
#     image_file('../images/dest_dendrogram.svg')
