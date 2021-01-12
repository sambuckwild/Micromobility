import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import folium 
from folium.plugins import HeatMap
from scipy.cluster.hierarchy import dendrogram
from clean_data import load_data, drop_cols_update_names, cols_to_datetime
from model import coord_location_array, kmeans_model, calc_silhouette_score 
from model import hierarchical_cluster_model, cluster_center_df
from eda_plotting_mapping import location_heat_map

def silhouette_score_plot(ax, sil_score_lst, color, label, title):
    ax.plot(range(2,10), sil_score_lst, 'o--', c = color, label=label)
    ax.set_xlabel('K', fontsize=18)
    ax.set_ylabel('Silhouette Score', fontsize=18)
    ax.set_title(title, fontsize=20)
    ax.legend()

def kmeans_scatter_plot(ax, cluster_array, color, size, label, title):
    '''scatter plot of geo-locations and/or cluster centers'''
    ax.scatter(cluster_array[:,0], cluster_array[:,1], s=size, 
                color=color, label=label)
    ax.set_xlabel('Latitude', fontsize=16)
    ax.set_ylabel('Longtitude', fontsize=16)
    ax.set_title(title, fontsize=20)
    ax.legend()

def dendrogram_plot(cluster, ax, level_num, trunc_mode, color_thresh, title):
    '''plot of heiracrchical clustering model'''
    dendrogram(cluster, ax, p=level_num, truncate_mode=trunc_mode,
                color_threshold=color_thresh)
    plt.xticks(fontsize=12)
    plt.title(title, fontsize=24)

def image_file(filepath):
    return plt.savefig(filepath, transparent=False, bbox_inches='tight', format='svg', dpi=1200)

def map_html_file(map_name, filepath):
    return map_name.save(filepath)
    
if __name__ == '__main__':

    # read in week long cleaned dataframe

    scooter_june_pride = load_data('../data/small_scooter.csv')
    scooter_june_pride = drop_cols_update_names(scooter_june_pride, ['Unnamed: 0'])
    scooter_june_pride = cols_to_datetime(scooter_june_pride, ['Start_Time', 'End_Time'])

    #create array of origin and destination coordinates for rides

    origin_array = coord_location_array(scooter_june_pride, 
                        'Start_Centroid_Latitude', 'Start_Centroid_Longitude')
    destination_array = coord_location_array(scooter_june_pride,
                            'End_Centroid_Latitude', 'End_Centroid_Longitude')

    #kmeans model, calculate silhouette scores, and create cluster center dataframe

    origin_kmeans = kmeans_model(origin_array)
    dest_kmeans = kmeans_model(destination_array)
    origin_sil_scores = [calc_silhouette_score(i, origin_array) for i in range(2,10)]
    dest_sil_scores = [calc_silhouette_score(i, destination_array) for i in range(2,10)]
    origin_clusters = origin_kmeans.cluster_centers_
    origin_clust_df = cluster_center_df(origin_clusters, ['lat', 'lon'])

    '''Silhouette Score Plots to determine number of clusters'''
    fig, ax = plt.subplots(figsize=(10,6))
    silhouette_score_plot(ax, origin_sil_scores, 'b', 'Ride Origins', 
                        'Silhouette Score vs K - Scooter Rides')
    silhouette_score_plot(ax, dest_sil_scores, 'm', 'Ride Destinations', 
                        'Silhouette Score vs K - Scooter Rides')
    image_file('../images/origin_dest_sil_plot.svg')

    #create hierarchical clustering model to plot as dendrogram

    origin_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                origin_array)
    
    '''Dendrogram Plot of hierarchical clustering model to determine number of clusters'''
    fig, ax = plt.subplots(figsize=(10,6))
    kmeans_scatter_plot(ax, origin_clusters, 'b', 75, 'Cluster Centers', 
                    'Ride Origins & K-Means Model Cluster Centers')
    kmeans_scatter_plot(ax, origin_array, 'grey', 8, 'Rider Origins', 
                    'Ride Origins & K-Means Model Cluster Centers')

    # heat map with origin cluster centers mapped on top

    chi_map3 = folium.Map(location=[41.88955765, -87.71819668], zoom_start=12)
    for i, row in origin_clust_df.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        popup=row['name']).add_to(chi_map3)
    origin_heat_map2 = location_heat_map(scooter_june_pride, 'Start_Centroid_Latitude', 
                            'Start_Centroid_Longitude', 'Ride Origins')
    origin_heat_map2 = chi_map3.add_child(origin_heat_map2)
    map_html_file(origin_heat_map2, '../images/origin_cluster_heat_map.html')

    

    