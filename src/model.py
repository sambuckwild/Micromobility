import pandas as pd 
import numpy as np
import folium
from folium.plugins import HeatMap
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import silhouette_score
from datetime import datetime
from scooter_clean import load_data, drop_cols_update_names, cols_to_datetime
from plotting_mapping import image_file


def coord_location_array(df, lat_col, long_col):
    location_lst = df[[lat_col, long_col]]
    array = location_lst.to_numpy()
    return array

def kmeans_model(array, n_clust=8):
    kmeans = KMeans(n_clusters=n_clust)
    kmeans.fit(array)
    return kmeans

def calc_silhouette_score(nclust, array):
    kmeans = KMeans(n_clusters = nclust, 
                init = 'random', 
                n_init = 10, 
                max_iter = 100, 
                n_jobs = -1)
    kmeans.fit(array)
    sil_avg = silhouette_score(array, kmeans.labels_)
    return sil_avg

def silhouette_plot(ax, sil_score_lst, color, label, title):
    ax.plot(range(2,10), sil_score_lst, 'o--', c = color, label=label)
    ax.set_xlabel('K', fontsize=18)
    ax.set_ylabel('Silhouette Score', fontsize=18)
    ax.set_title(title, fontsize=20)
    ax.legend()

def kmeans_scatter_plot(ax, cluster_array, color, size, label, title):
    ax.scatter(cluster_array[:,0], cluster_array[:,1], s=size, 
                color=color, label=label)
    ax.set_xlabel('Latitude', fontsize=16)
    ax.set_ylabel('Longtitude', fontsize=16)
    ax.set_title(title, fontsize=20)
    ax.legend()

def cluster_center_df(cluster_array, col_lst):
    df = pd.DataFrame(cluster_array, columns=col_lst)
    name = ['cluster' + str(idx+1) for idx in range(0,len(df))]
    df['name'] = name
    return df

def hierarchical_cluster_model(dist_metric, link_method, array):
    distmetric = dist_metric
    linkmethod = link_method
    dist = pdist(array, metric=distmetric)
    clust = linkage(dist, method=linkmethod)
    return clust

def dendrogram_plot(cluster, ax, level_num, trunc_mode, color_thresh, title):
    dendrogram(cluster, ax, p=level_num, truncate_mode=trunc_mode,
                color_threshold=color_thresh)
    plt.xticks(fontsize-12)
    plt.title(title, fontsize=24)

def get_cluster_geo_df(kmeans_model, n_clust):
    cluster_centers = kmeans_model.cluster_centers_
    cluster_lat_lon = [cluster_centers[i][2:4] for i in range(0,n_clust)]
    clust_df = pd.DataFrame(data=cluster_lat_lon, columns=['lat', 'lon'])
    name = ['cluster ' + str(idx + 1) for idx in range(0, len(clust_df))]
    clust_df['name'] = name
    return clust_df


if __name__ == '__main__':
    # read in week long cleaned dataframe
    scooter_june_pride = load_data('../data/small_scooter.csv')
    scooter_june_pride = drop_cols_update_names(scooter_june_pride, ['Unnamed: 0'])
    scooter_june_pride = cols_to_datetime(scooter_june_pride, ['Start_Time', 'End_Time'])

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
    image_file('../images/origin_dest_sil_plot.svg')

    # run the models again with 8 clusters for origin and 5 for destination
    origin_kmeans = kmeans_model(origin_array, n_clust=8)
    origin_clusters = origin_kmeans.cluster_centers_
    dest_kmeans = kmeans_model(destination_array, n_clust=5)
    dest_clusters = dest_kmeans.cluster_centers_

    fig, ax = plt.subplots(figsize=(10,6))
    kmeans_scatter_plot(ax, origin_clusters, 'b', 75, 'Cluster Centers', 
                    'Ride Origins & K-Means Model Cluster Centers')
    kmeans_scatter_plot(ax, origin_array, 'grey', 8, 'Rider Origins', 
                    'Ride Origins & K-Means Model Cluster Centers')

    origin_clust_df = cluster_center_df(origin_clusters, ['lat', 'lon'])
    
    # hierarchical clustering model
    origin_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                origin_array)
    dest_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                destination_array)