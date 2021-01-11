<div align="center">  
<header>
    <h1>Electric Micromobility <br>
    Scooting Towards Equitable, Carbon-Free Transportation</h1>
  </header>
<div align='left'>

![](images/micromobilitycopy.jpg)   
[source](https://www.theverge.com/2019/11/19/20972322/ojo-gotcha-acquisition-electric-scooter-bike-shared-micromobility)

## Project Goals + Questions
Car rideshare has gained momentum exponentially in the last few years, and now we have seen the beginning of the shared micromobility boom. How can shared micromobility companies benefit as much as their car counterparts? I wanted to explore this further.  
-  How can the scooter companies increase their profit? 
-  Should the companies invest in someone moving scooters midday to increase usage? 
-  Are there certain days of the week, times of the day, or areas of the city the scooters scooters are used most often?
-  Which transit stops have the highest usage rate? 
-  Are the scooters being used in areas with supporting infrastructure already in place such as bike lanes?   

## Table of Contents
1. [Background and Motivation](#background-and-motivation)
2. [Raw Data and Data Munging ](#raw-data-and-data-munging)
3. [Exploratory Data Analysis](#exploratory-data-analysis)
4. [Analysis](#analysis)
5. [Future Work](#future-work)


## Background and Motivation   

![](images/micromobilityinfographic-01.png)
<font size ="-1">*Figure 1: Micromobility Infographic (By Alison Blaine)*</font><br>  

Micromobility describes a range of small, lightweight devices operated at speeds below 26 miles per hour either owned or rented by the user. Micromobility includes bicycles, e-bikes, scooters, e-scooters, roller blades, skateboards, e-skateboards, and mono-wheels, and is an emerging transportation sector experiencing a lot of growth and evolution. <br>  

Urbanists and technologist agree, shared micromobility is one of the greatest inventions to disrupt transportation in the built environment. These battery-powered, carbon-free devices are a welcomed option for pedestrians looking for a fun, quick way to get around town. Micromobility also helps make transit more accessible and a viable option for more people by supporting first and last mile travel—a known gap within our transportation system. Due to the low cost to operate the shared variety, micromobility is being touted as a more equitable mode of transportation. <br>  

As a scooter enthusiast, I would like to understand the most profitable places for scooters to be deployed each morning in regard to transit stops, high-traffic areas, and areas with less car ownership or usage.   
 
![](images/microbanner.png)   
<font size ="-1">*Figure 2: Scooters in Action (Pictures + Design by Samantha Buck)*</font><br> 

## Raw Data and Data Munging  

### Initial Data   

I retrieved e-scooter trip data for the 2019 pilot in Chicago, Illinois, from the City’s open [data source](https://data.cityofchicago.org/Transportation/E-Scooter-Trips-2019-Pilot/2kfw-zvte). I also obtained Chicago bicycle lane spatial [data](https://data.cityofchicago.org/Transportation/Bike-Routes/3w5d-sru8), as well as [bus](https://data.cityofchicago.org/Transportation/CTA-Ridership-Avg-Weekday-Bus-Stop-Boardings-in-Oc/mq3i-nnqe) and L [rail](https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f) ridership datasets from the CTA's open source portal. The bus dataset was most recently updated in 2012, however the comprehensive rail dataset was only available for 2001. I have obtained the 2001 bus dataset as well to be able to make some assumptions, with population growth considered, for current ridership on both transit systems to be able to compare to the 2019 scooter dataset. I have reached out to the CTA to obtain more recent data and am waiting on a reply for my Freedom of Information Act request. <br>  

| Trip ID                              | Start Time             | End Time               | Trip Distance | Trip Duration | Accuracy | Start Census Tract | End Census Tract | Start Community Area Number | End Community Area Number | Start Community Area Name | End Community Area Name | Start Centroid Latitude | Start Centroid Longitude | Start Centroid Location                    | End Centroid Latitude | End Centroid Longitude | End Centroid Location                      |
|--------------------------------------|------------------------|------------------------|---------------|---------------|----------|--------------------|------------------|-----------------------------|---------------------------|---------------------------|-------------------------|-------------------------|--------------------------|--------------------------------------------|-----------------------|------------------------|--------------------------------------------|
| 758e9d21-609f-5479-8e2c-5e8f64258202 | 07/01/2019 05:00:00 PM | 07/01/2019 05:00:00 PM | 421      | 3      | 1   |      NaN        |     NaN        |   NaN      |    NaN         |    NaN        |  NaN |   NaN       |     NaN         |     NaN       |     NaN     |          NaN  |   NaN         |
| ff33490c-254a-5af2-9315-d6b2a45b07f7 | 06/29/2019 06:00:00 PM | 06/29/2019 06:00:00 PM | 6318      | 31      | 1     |    NaN      |   NaN     |    NaN       |   NaN     |  NaN    |     NaN        | NaN     | NaN  |   NaN      | NaN     | NaN      |   NaN          |
| f8a25729-e853-40f3-9200-7eea9f9c45f2 | 09/16/2019 01:00:00 PM | 09/16/2019 01:00:00 PM | 77        | 732    | 10    |     NaN          |  NaN       |    NaN            | 25            |    NaN           | AUSTIN        |     NaN           |     NaN             |   NaN       | 41.8941012961134      | -87.7631118242259      | POINT (-87.7631118242259 41.8941012961134) |
| 11d42b99-e839-346c-11d4-2b99e839346c | 06/24/2019 07:00:00 PM | 06/24/2019 07:00:00 PM | 917       | 359    | 10       |      NaN        |    NaN     | 25             | 25          | AUSTIN        | AUSTIN            | 41.8941012961134        | -87.7631118242259        | POINT (-87.7631118242259 41.8941012961134) | 41.8941012961134      | -87.7631118242259      | POINT (-87.7631118242259 41.8941012961134) |
| 0c226130-0fa6-518f-8fe6-219b9fa5f42f | 07/12/2019 07:00:00 PM | 07/12/2019 07:00:00 PM | 0       | 218      | 0     |      NaN      |    NaN       | 21        | 21      | AVONDALE          | AVONDALE           | 41.938665887698         | -87.7112106378686        | POINT (-87.7112106378686 41.938665887698)  | 41.938665887698       | -87.7112106378686      | POINT (-87.7112106378686 41.938665887698)  |

<font size ="-1">*Figure 3: Five rows from initial e-scooter pilot dataset*</font><br>

### Data Munging    

Each data file is in a CSV format, and upon initial look didn't need too much cleaning except to remove rows with NaN values for coordinates, trip distance and/or trip duration. The scooter and bike lane sets have coordinates that can be used for mapping purposes. The bus and rail datasets need some work to try to create new ones estimating 2019 data and to be able to compare the scooter data with ridership--waiting on new data from the CTA currently, but may do a future project creating a predictive model to obtain the data.   

#### Assumptions  
After a more thorough review of the scooter pilot data, there were some assumptions/decisions I made for my model and thus I decided to drop a few columns and filter out more of the data:  
-  Each ride is indepedent of every other ride
-  ```Census Tract``` and ```Community Area Name/Number``` were not as important feautres as the origin/destination coordinates
-  ```Start and End Location``` columns had the incorrect pairing of the coordinates
-  ```Trip Distance``` was originally in meters, each value was divided by 1609 to be shown in miles
-  ```Trip Distance``` of more than 25 miles was removed from the dataset as the timing didn't match up and a trip of more than 25 miles on a scooter is very unlikely so seems to be incorrect data  
-  ```Trip Duration``` was originally in seconds, each value was divided by 60 to be shown in minutes
-  Similarly, ```Trip Duration``` of less than 2 minutes or more than 8 hours was removed as less than 2 minutes is most likely a broken/uncharged scooter and more than 8 hours is someone keeping a scooter unlocked for instance from riding to work and then riding back at the end of the day (won't help in the question of should they be moved during the day)  

I still had over 590,000 data points after cleaning the data and filtering out bad data, so I decided to focus in on just one week of data: **Pride Week in June 2019 which was 6/21/2019 - 6/30/2019**.  

|   | Trip_ID                              | Start_Time          | End_Time            | Trip_Distance      | Trip_Duration      | Accuracy | Start_Centroid_Latitude | Start_Centroid_Longitude | End_Centroid_Latitude | End_Centroid_Longitude | Day_of_Week | Time_of_Day |
|---|--------------------------------------|---------------------|---------------------|--------------------|--------------------|----------|-------------------------|--------------------------|-----------------------|------------------------|-------------|-------------|
| 0 | 11d42b99-e839-346c-11d4-2b99e839346c | 2019-06-24 19:00:00 | 2019-06-24 19:00:00 | 0.5699192044748290 | 5.983333333333330  | 10       | 41.8941012961134        | -87.7631118242259        | 41.8941012961134      | -87.7631118242259      | 0           | 19          |
| 1 | c46c5b1f-d7a1-5c11-96b6-bb8bfa2d4fa3 | 2019-06-21 18:00:00 | 2019-06-21 19:00:00 | 0.4698570540708520 | 46.833333333333300 | 0        | 41.95358181896          | -87.72345248206660       | 41.95358181896        | -87.72345248206660     | 4           | 18          |
| 2 | 3ad30b66-b615-404b-ada2-92cfb30dd32b | 2019-06-21 21:00:00 | 2019-06-21 21:00:00 | 0.8247358607830950 | 4.0                | 152      | 41.95358181896          | -87.72345248206660       | 41.95358181896        | -87.72345248206660     | 4           | 21          |
| 3 | 8574e87e-d881-4468-bf79-f7e62f268f4d | 2019-06-21 18:00:00 | 2019-06-21 19:00:00 | 1.6948415164698600 | 22.416666666666700 | 10       | 41.95358181896          | -87.72345248206660       | 41.95358181896        | -87.72345248206660     | 4           | 18          |
| 4 | 9b79b345-1492-40f4-85a6-fee83c5a6ffc | 2019-06-26 18:00:00 | 2019-06-26 18:00:00 | 0.9919204474829090 | 5.316666666666670  | 152      | 41.95358181896          | -87.72345248206660       | 41.95358181896        | -87.72345248206660     | 2           | 18          |

<font size ="-1">*Figure 4: Five rows from cleaned scooter data June Pride Week 2019*</font><br>

## Exploratory Data Analysis

After cleaning the data, I started exploring it by looking at the spread of trip distances and durations, the frequency of rides--day of week and hour of the day--and by oberserving the spatial relationship between ride origins and destinations.  

![](images/trip_distance_hist.svg)   

![](images/trip_duration_hist.svg)   
> The majority of rides went less than 2 miles and were less than 15 minutes long.

![](images/day_of_week_bar.svg)  

![](images/hour_of_day_bar1.svg)
> Friday & Saturday look to be the prime days for scooter rides, and over all days in the week afternoon/evening is the prime time.

![](images/day_hour_line_plot.svg)   
> This shows almost a cyclic nature for rides Monday-Thursday around the end of the workday/early evening, with peak rides on Friday & Saturday around lunchtime/early afternoon, and again on Sunday a similar peak to the weekdays just shifted earlier around brunch time.

| **Scooter Ride Origins Heat Map**   |  **Scooter Ride Destinations Heat Map** |
|  ------   |   -----   |
|![](images/origin_heat_map.png)  | ![](images/dest_heat_map.png) |  
> Both ride origins and destinations seem to be clustered around similar areas in the city, just that more rides start further out and end up closer to downtown as one would expect.
> We can see that certain areas further out from the downtown area have similar heat map signatures for origins and destinations so maybe the same people use scooters to get into town and then back home.


## Analysis

I chose to use unsupervised clustering analysis to extrapolate hidden relationships in the scooter ride data. Due to the nature of the data, hard clustering was used comparing both K-Means and Hierarchical clustering methods. 

#### K-Means Clustering

Initial running of the model which produced 8 cluster centers, along with the silhouette score for varying number of clusters to determine how many to use in my adjusted model are shown below.

|**Ride Origin Cluster Centers**|**Origin Silhouette Score**|**Ride Destination Cluster Centers**|**Destination Silhouette Score**|
| :----------------: | :------------------------: | :------------------------------------------: |  :-------------:  |
|  41.92271055, -87.69864685    | 2 clusters: 0.527 |  41.90502859, -87.67485789 | 2 clusters: 0.514| 
|  41.88322404, -87.65717622   |  3 clusters: 0.471|   41.93554794 -87.72108325|   3 clusters: 0.462 |
|   41.89384565, -87.76146354 |   4 clusters: 0.532 |    41.8912974, -87.71854302|   4 clusters: 0.501 |
|   41.8626154,  -87.71611382  |  5 clusters: 0.543  |   41.92274303, -87.69833183|   5 clusters: 0.518   |
|  41.93383835, -87.7709733  | 6 clusters: 0.517 |   41.93433698, -87.77101021  |    6 clusters: 0.519 |
|  41.90517536, -87.67633932 |  7 clusters: 0.529   |  41.87932401, -87.65787626  |     7 clusters: 0.508 |
|  41.92835925, -87.72146241|  8 clusters: 0.525  |   41.8485868, -87.71491064 |    8 clusters: 0.436  |
|  41.85610043, -87.66720712] |  9 clusters: 0.563  | 41.8936009, -87.76217343 |   9 clusters: 0.527 |   
<br>   

![](images/origin_dest_sil_plot.svg)   


> Based on the silhouette score plot, the largest scores--meaning tighter, non-overlapping clusters--for ride origins and destinations are 4,5,8 and 5,6 respectively.   

I ran my model again using 8 clusters for origins and 5 clusters for destinations to obtain the cluster centers. The centers are plotted below on a scatter plot of the rides along with overlaying the original ride origin or destination heat maps.  

| **Ride Origins + Cluster Centers Scatter Plot**   |  **Ride Origins Heat Map + Cluster Centers Markers** |
|  ------   |   -----   |
|![](images/kmeans_origin_scatter.svg)  | ![](images/cluster_origin_heat_map.png) |   

| **Ride Destinations + Cluster Centers Scatter Plot**   |  **Ride Destinations Heat Map + Cluster Centers Markers** |
|  ------   |   -----   |
|![](images/kmeans_dest_scatter.svg)  | ![](images/cluster_dest_heat_map.png) |   

#### Hierarchical Clustering

I initially ran the model with the distance metric as *Euclidean distance* to see how it compared to the K-Means model. I used the same number of clusters, 8 for origins and 5 for destinations, to visualize them on the below dendrograms.  

![](images/origin_dendrogram.svg)  

![](images/dest_dendrogram.svg)   

In conclusion, based on the model outcomes and EDA I would say the morning scooter deployment seems to cover the area fairly well meaning there is no significant loss in profit. The bulk of the rides are happening within an 8-hour window, this is where the company may need to move the scooters again to make sure ride opportunities are not missed and/or they may need to charge the scooters during this window due to the amount of rides. If the company has data surrounding scooter battery life, this would be another helpful feature to determine if ridership declined due to scooters having little or no bettery life. 

## Future Work 
I would love to be able to use these cleaning and analysis pipelines on other cities’ scooter pilot data so a new market can see the value of adding shared micromobility, as well as continue exploring the future steps listed below.  


Future analysis could be:  
- Explore other distance metrics with my hierarchical clustering  model
- Run both models with more features included in the dataset, currently just ran on origin and destination coordinates
- Run my model and analysis on the entire cleaned dataset, not just the focused June Pride Week
- Compare scooter trip spatial data with bike lane infrastructure
- Visualize most trafficked transit stops
- Supervised machine Learning predictive model to obtain transit ridership data for comparison with scooter data; can then compare model to updated data I receive from the CTA
- Hypothesis test or other statistical analyses on scooter usage
- Create a predictive machine learning model using available scooter data to predict the best locations for drop off in the morning—which locations have the highest profitability potential, utilization rates, connect the most people to transit, etc.
![](images/SantaMonicascootercorral.jpg)  
<font size ="-1">*Figure 5: Micromobility infrastructure + e-scooter rider*</font><br>
[source](https://chi.streetsblog.org/2019/05/01/chicago-will-launch-a-pilot-with-2500-dockless-scooters-on-june-15/)
<br>


