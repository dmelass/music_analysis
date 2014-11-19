# Dara Elass

import pickle
import sys
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
from auth_ids import plotly_username, plotly_key

py.sign_in(plotly_username,plotly_key)

# functions
def create_pickle(data, filename):
    with open(filename,'w') as picklefile:
        pickle.dump(data,picklefile)

def load_pickle(filename):
    data_name = filename[:-4]
    with open(filename,'r') as picklefile:
        data_name = pickle.load(picklefile)
    return data_name

# exploratory analysis
songs = load_pickle('all_songs.pkl')
focus_fields = ['duration','tempo','speechiness','instrumentalness','key','mode'] # fields to focus on
focus_fields_2 = ['energy','liveness','danceability','valence']
all_fields = focus_fields + focus_fields_2
used_countries = ['lebanon','egypt','united states','france','italy','nigeria','mexico','china','japan','india','cuba']
grouped_songs = songs.groupby('country')
songs_per_country = grouped_songs.size()
total_songs = [songs_per_country[country] for country in used_countries]

# # get counts
# print '------------------------'
# print 'count of songs per country:'
# print songs_per_country

# # get mean values
# mean_by_country = grouped_songs.mean()
# print '------------------------'
# print 'mean values by country:' 
# print mean_by_country # not all fields are showing

# # get max values
# max_by_country = grouped_songs.max()
# print '------------------------'
# print 'max values by country:' 
# print max_by_country

# # get min values
# min_by_country = grouped_songs.min()
# print '------------------------'
# print 'min values by country:' 
# print min_by_country

# # create box plots of each focus field by country
# for field in focus_fields:
# 	data = Data()
# 	for country in used_countries:
# 		idx = songs['country'].str.contains(country)
# 		data.append(Box(y=songs[idx][field],name=country))
# 	py.iplot(data,filename =field+' by country')
# 	print 'finished creating plot for ' + field

# # create box plots of each focus field by country (using focus fields 2)
# for field in focus_fields_2:
# 	data = Data()
# 	for country in used_countries:
# 		idx = songs['country'].str.contains(country)
# 		data.append(Box(y=songs[idx][field],name=country))
# 	py.iplot(data,filename =field+' by country')
# 	print 'finished creating plot for ' + field

# # create bar chart for mode (because it's a binary variable)
# grouped_country_mode = songs.groupby(['country','mode'])
# trace1 = Bar(x=used_countries,y=[grouped_country_mode.country.count()[country][0]/float(total_songs[i]) for i, country in enumerate(used_countries)],name='Minor') # mode = 0
# trace2 = Bar(x=used_countries,y=[grouped_country_mode.country.count()[country][1]/float(total_songs[i]) for i, country in enumerate(used_countries)],name='Major') # mode = 1
# data = Data([trace1, trace2])
# layout = Layout(barmode='group')
# fig = Figure(data=data, layout=layout)
# py.plot(fig, filename='mode by country normalized')

# # create bar chart for key (because looking at the keys as letters and distribution is better than box plot)
# grouped_country_key = songs.groupby(['country','key'])
# data = Data()
# keys = ['c','c-sharp','d','e-flat','e','f','f-sharp','g','a-flat','a','b-flat','b']
# for i in range(12): # there are 11 keys (0-11: c,c#,d,e-flat,f,f#,g,a-flat,a,b-flat,b)
# 	data.append(Bar(x=used_countries,y=[grouped_country_key.country.count()[country][i] for country in used_countries],name=keys[i]))
# layout = Layout(barmode='group')
# fig = Figure(data=data, layout=layout)
# py.plot(fig, filename='key by country - bar')

# # create line graph for keys by country
# grouped_country_key = songs.groupby(['country','key'])
# data = Data()
# keys = ['c','c-sharp','d','e-flat','e','f','f-sharp','g','a-flat','a','b-flat','b']
# for i in range(12): # there are 11 keys (0-11: c,c#,d,e-flat,f,f#,g,a-flat,a,b-flat,b)
# 	data.append(Scatter(x=used_countries,y=[grouped_country_key.country.count()[country][i]/float(total_songs[j]) for j,country in enumerate(used_countries)],name=keys[i],mode='lines+markers'))
# py.plot(data, filename='key by country - line')

# starting analysis/clustering









