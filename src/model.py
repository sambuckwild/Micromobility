import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage
from sklearn.metrics import silhouette_score
from datetime import datetime
from clean_data import load_data, drop_cols_update_names, cols_to_datetime

def coord_location_array(df, lat_col, long_col):
    '''create array of location coordinates from dataframe'''
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

def cluster_center_df(cluster_array, col_lst):
    '''create dataframe of coordinates for cluster center of only 
        lattitude/longitude data'''
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

def get_cluster_geo_df(kmeans_model, n_clust):
    '''create dataframe of coordinates for cluster centers from kmeans
        (for 6 feautres with lattitude/longitude as columns 2&3'''
    cluster_centers = kmeans_model.cluster_centers_
    cluster_lat_lon = [cluster_centers[i][2:4] for i in range(0,n_clust)]
    clust_df = pd.DataFrame(data=cluster_lat_lon, columns=['lat', 'lon'])
    name = ['cluster ' + str(idx + 1) for idx in range(0, len(clust_df))]
    clust_df['name'] = name
    return clust_df

if __name__ == '__main__':

    # read in week long cleaned dataframe for initial modeling & create coordinate arrays

    scooter_june_pride = load_data('../data/small_scooter.csv')
    scooter_june_pride = drop_cols_update_names(scooter_june_pride, ['Unnamed: 0'])
    scooter_june_pride = cols_to_datetime(scooter_june_pride, ['Start_Time', 'End_Time'])

    origin_array = coord_location_array(scooter_june_pride, 
                        'Start_Centroid_Latitude', 'Start_Centroid_Longitude')
    destination_array = coord_location_array(scooter_june_pride,
                            'End_Centroid_Latitude', 'End_Centroid_Longitude')
    
    #kmeans models and silhouette scores calculated for week long data

    origin_kmeans = kmeans_model(origin_array)
    print('cluster centers:{}'.format(origin_kmeans.cluster_centers_)) 
    dest_kmeans = kmeans_model(destination_array)
    print('cluster centers:{}'.format(dest_kmeans.cluster_centers_))

    origin_sil_scores = [calc_silhouette_score(i, origin_array) for i in range(2,10)]
    dest_sil_scores = [calc_silhouette_score(i, destination_array) for i in range(2,10)]

    # run the models again with 8 clusters for origin and 5 for destination (pride week)

    origin_kmeans = kmeans_model(origin_array, n_clust=8)
    origin_clusters = origin_kmeans.cluster_centers_
    dest_kmeans = kmeans_model(destination_array, n_clust=5)
    dest_clusters = dest_kmeans.cluster_centers_

    #create dataframe of cluster centers from kmeans model

    origin_clust_df = cluster_center_df(origin_clusters, ['lat', 'lon'])
    
    # hierarchical clustering model (week long data) of just coordinate arrays

    origin_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                origin_array)
    dest_hier_clust = hierarchical_cluster_model('euclidean', 'complete',
                                                destination_array)