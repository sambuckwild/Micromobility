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

from clean_data import *
from model_plotting_mapping import *
from eda_plotting_mapping import *
from model import *


if __name__ == '__main__':
    
    # clean full dataset with only six features

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

