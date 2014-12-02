#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dara Elass

import pickle
import sys
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
from auth_ids import plotly_username, plotly_key
from sklearn.cluster import DBSCAN,MiniBatchKMeans
from collections import Counter
import numpy as np
from datetime import datetime
from sklearn.metrics import pairwise_distances
import operator 
from sklearn.preprocessing import scale
from matplotlib import pyplot as plt
from collections import defaultdict
import os

py.sign_in(plotly_username,plotly_key)

# define functions
def create_pickle(data, filename):
    with open(filename,'w') as picklefile:
        pickle.dump(data,picklefile)

def load_pickle(filename):
    data_name = filename[:-4]
    with open(filename,'r') as picklefile:
        data_name = pickle.load(picklefile)
    return data_name

def get_basic_data(data):
	mean = data.mean()
	count = data.size()
	maximums = data.max()
	minimums = data.min()
	return mean, count, maximums, minimums

def create_clusters(X):
    model = DBSCAN(eps=0.7,min_samples=3)
    clusters = model.fit_predict(X)	
    create_pickle(clusters,'clusters.pkl')
    return model,clusters

def calc_cluster_sizes(clusters):
    cluster_sizes_unordered = Counter(clusters)
    cluster_sizes = sorted(cluster_sizes_unordered.items(), key = operator.itemgetter(1), reverse=True)
    return cluster_sizes

###################################
# define variables/data frames
###################################
songs = load_pickle('all_songs.pkl')
focus_fields = ['duration','tempo','speechiness','instrumentalness','key','mode'] # fields to focus on
focus_fields_2 = ['energy','liveness','danceability','valence']
all_fields = focus_fields + focus_fields_2
used_countries = ['lebanon','egypt','united states','france','italy','nigeria','mexico','china','japan','india','cuba']
grouped_songs = songs.groupby('country')
songs_per_country = grouped_songs.size()
total_songs = [songs_per_country[country] for country in used_countries] # array of all numbers

###################################
# exploratory analyses
###################################

mean,count,maxes,mins = get_basic_data(grouped_songs)

# create bar graph of number of songs collected per country
data = Data([Bar(x=used_countries,y=total_songs)])
py.plot(data,filename = 'songs per country')

# create box plots of each focus field by country
for field in focus_fields:
	data = Data()
	for country in used_countries:
		idx = songs['country'].str.contains(country)
		data.append(Box(y=songs[idx][field],name=country))
	py.iplot(data,filename =field+' by country')
	print 'finished creating plot for ' + field

# create box plots of each focus field by country (using focus fields 2)
for field in focus_fields_2:
	data = Data()
	for country in used_countries:
		idx = songs['country'].str.contains(country)
		data.append(Box(y=songs[idx][field],name=country))
	py.iplot(data,filename =field+' by country')
	print 'finished creating plot for ' + field

# create bar chart for mode (because it's a binary variable)
grouped_country_mode = songs.groupby(['country','mode'])
trace1 = Bar(x=used_countries,y=[grouped_country_mode.country.count()[country][0]/float(total_songs[i]) for i, country in enumerate(used_countries)],name='Minor') # mode = 0
trace2 = Bar(x=used_countries,y=[grouped_country_mode.country.count()[country][1]/float(total_songs[i]) for i, country in enumerate(used_countries)],name='Major') # mode = 1
data = Data([trace1, trace2])
layout = Layout(barmode='group')
fig = Figure(data=data, layout=layout)
py.plot(fig, filename='mode by country normalized')

# create bar chart for key (because looking at the keys as letters and distribution is better than box plot)
grouped_country_key = songs.groupby(['country','key'])
data = Data()
keys = ['c','c-sharp','d','e-flat','e','f','f-sharp','g','a-flat','a','b-flat','b']
for i in range(12): # there are 11 keys (0-11: c,c#,d,e-flat,f,f#,g,a-flat,a,b-flat,b)
	data.append(Bar(x=used_countries,y=[grouped_country_key.country.count()[country][i] for country in used_countries],name=keys[i]))
layout = Layout(barmode='group')
fig = Figure(data=data, layout=layout)
py.plot(fig, filename='key by country - bar')

# create line graph for keys by country
grouped_country_key = songs.groupby(['country','key'])
data = Data()
keys = ['c','c-sharp','d','e-flat','e','f','f-sharp','g','a-flat','a','b-flat','b']
for i in range(12): # there are 11 keys (0-11: c,c#,d,e-flat,f,f#,g,a-flat,a,b-flat,b)
	data.append(Scatter(x=used_countries,y=[grouped_country_key.country.count()[country][i]/float(total_songs[j]) for j,country in enumerate(used_countries)],name=keys[i],mode='lines+markers'))
py.plot(data, filename='key by country - line')

###################################
# starting analysis/clustering
###################################

for filename in os.listdir(os.getcwd()):
    if 'ClusterNumber' in filename:
        os.remove(filename)

features = [0,1,2,3,4,5,6,7,8,9,10,11,'energy','liveness','tempo','speechiness','acousticness','danceability','instrumentalness','duration','loudness','valence','mode']
key_dummies = pd.get_dummies(songs['key']) # create dummies
songs = key_dummies.combine_first(songs) # merge data frames
# songs = songs.dropna()
X = songs[features] # get features columns
X = X.dropna() # make sure there are no NA values
model,clusters = create_clusters(scale(X)) # create clusters/get array with cluster assignment
cluster_sizes = calc_cluster_sizes(clusters)
print 'cluster sizes:', cluster_sizes
cluster_sizes = calc_cluster_sizes(clusters)

countries_count = defaultdict(int)
for country in songs.country:
    countries_count[country] += 1

for p,(cluster_number,cluster_size) in enumerate(cluster_sizes[:26]): # look at the 10 biggest clusters
    if cluster_number != -1:
        countries_dist = []
        energy_dist = []
        liveness_dist = []
        tempo_dist = []
        speechiness_dist = []
        acousticness_dist = []
        danceability_dist = []
        instrumentalness_dist = []
        duration_dist = []
        loudness_dist = []
        valence_dist = []
        mode_dist = []
        key_dist = []
        print '---------------------------------------'
        print 'cluster:',cluster_number
        print 'number of songs:', cluster_size
        X_this_cluster = X[clusters == cluster_number]
        indices_of_cluster_songs = X_this_cluster.index.tolist() 
        print indices_of_cluster_songs
        for j in range(cluster_size):
            id_of_closest = indices_of_cluster_songs[j]
            countries_dist.append(songs.loc[id_of_closest]['country'])
            energy_dist.append(songs.loc[id_of_closest]['energy'])
            liveness_dist.append(songs.loc[id_of_closest]['liveness'])
            tempo_dist.append(songs.loc[id_of_closest]['tempo'])
            speechiness_dist.append(songs.loc[id_of_closest]['speechiness'])
            acousticness_dist.append(songs.loc[id_of_closest]['acousticness'])
            danceability_dist.append(songs.loc[id_of_closest]['danceability'])
            instrumentalness_dist.append(songs.loc[id_of_closest]['instrumentalness'])
            duration_dist.append(songs.loc[id_of_closest]['duration'])
            loudness_dist.append(songs.loc[id_of_closest]['loudness'])
            valence_dist.append(songs.loc[id_of_closest]['valence'])
            mode_dist.append(songs.loc[id_of_closest]['mode'])
            key_dist.append(songs.loc[id_of_closest]['key'])
            if j <= 10:
                print songs.loc[id_of_closest]['song_name'] + ' BY ' + songs.loc[id_of_closest]['artist_name'] + ' FROM ' + songs.loc[id_of_closest]['country']
            
        countries_dist_count = defaultdict(int)
        for country in countries_dist:
            countries_dist_count[country] += 1

        f, axarr = plt.subplots(3,4)
        axarr[0,0].bar(range(len(used_countries)),[countries_dist_count[country] for country in used_countries])
        axarr[0,0].set_title('Countries')
        axarr[0,0].set_xticklabels(used_countries)
        axarr[0,1].hist(songs.energy,normed=True)
        axarr[0,1].hist(energy_dist,normed=True)
        axarr[0,1].set_title('Energy')
        axarr[0,2].hist(songs.liveness.dropna(),normed=True)
        axarr[0,2].hist(liveness_dist,normed=True)
        axarr[0,2].set_title('Liveness')
        axarr[0,3].hist(songs.tempo,normed=True)
        axarr[0,3].hist(tempo_dist,normed=True)
        axarr[0,3].set_title('Tempo')

        axarr[1,0].hist(songs.speechiness.dropna(),normed=True)
        axarr[1,0].hist(speechiness_dist,normed=True)
        axarr[1,0].set_title('Speechiness')
        axarr[1,1].hist(songs.acousticness.dropna(),normed=True)
        axarr[1,1].hist(acousticness_dist,normed=True)
        axarr[1,1].set_title('Acousticness')
        axarr[1,2].hist(songs.danceability.dropna(),normed=True)
        axarr[1,2].hist(danceability_dist,normed=True)
        axarr[1,2].set_title('Danceability')
        axarr[1,3].hist(songs.instrumentalness.dropna(),normed=True)
        axarr[1,3].hist(instrumentalness_dist,normed=True)
        axarr[1,3].set_title('Instrumentalness')

        axarr[2,0].hist(songs.duration.dropna(),normed=True)
        axarr[2,0].hist(duration_dist,normed=True)
        axarr[2,0].set_title('Duration')
        axarr[2,1].hist(songs.loudness.dropna(),normed=True)
        axarr[2,1].hist(loudness_dist,normed=True)
        axarr[2,1].set_title('Loudness')
        axarr[2,2].hist(songs.valence.dropna(),normed=True)
        axarr[2,2].hist(valence_dist,normed=True)
        axarr[2,2].set_title('Valence')
        axarr[2,3].hist(songs['mode'].dropna(),normed=True)
        axarr[2,3].hist(mode_dist,normed=True)
        axarr[2,3].set_title('Mode')
        plt.savefig(str(p)+'_ClusterNumber_'+str(cluster_number)+'.png')

        plt.figure()
        plt.hist(songs.energy,normed=True)
        plt.hist(energy_dist,normed=True)
        plt.ylabel('frequency')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_energy.png')

        plt.figure()
        plt.hist(songs.instrumentalness.dropna(),normed=True)
        plt.hist(instrumentalness_dist,normed=True)
        plt.ylabel('frequency')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_instrumentalness.png')

        plt.figure()
        plt.hist(songs.tempo.dropna(),normed=True)
        plt.hist(tempo_dist,normed=True)
        plt.ylabel('frequency')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_tempo.png')

        plt.figure()
        plt.hist(songs.acousticness.dropna(),normed=True)
        plt.hist(acousticness_dist,normed=True)
        plt.ylabel('frequency')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_acousticness.png')

        plt.figure()
        plt.hist(songs.valence.dropna(),normed=True)
        plt.hist(valence_dist,normed=True)
        plt.ylabel('frequency')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_valence.png')

        plt.figure()
        plt.hist(songs.danceability.dropna(),normed=True)
        plt.hist(danceability_dist,normed=True)
        plt.ylabel('frequency')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_danceability.png')

        plt.figure()
        plt.bar(range(len(used_countries)),[countries_dist_count[country] for country in used_countries])
        plt.xticks(range(len(used_countries)), used_countries, rotation=45)        
        plt.ylabel('count')
        plt.xlabel('country')
        plt.savefig('ClusterNumber_'+str(cluster_number)+'_countries.png')

