# Dara Elass

from auth_ids import echonest_API_key, spotify_API_key
from pyechonest import song, artist, config
import requests
import json
from datetime import datetime
import time
import pickle
from collections import defaultdict
import pandas as pd
import numpy as np
import sys

config.ECHO_NEST_API_KEY = echonest_API_key

# functions
def create_pickle(data, filename):
    with open(filename,'w') as picklefile:
        pickle.dump(data,picklefile)

def load_pickle(filename):
    data_name = filename[:-4]
    with open(filename,'r') as picklefile:
        data_name = pickle.load(picklefile)
    return data_name

def get_artists_in_dict(parameters,dictionary):
        r = requests.get("http://developer.echonest.com/api/v4/artist/search?",params=parameters)
        r = r.json()
        print 'got request for country: ' + country + ' and start number: ' + str(the_start)
        for person in r['response']['artists']: # for each artist, get name and ID
            the_artist = person['name']
            the_artist_id = person['id']
            dictionary[country].append({the_artist_id:the_artist})    

def get_all_artists(countries,dictionary,num_artists):
    for country in countries:
        for i in range(num_artists/100):
            the_start = 100*i
            parameters = {'api_key':echonest_API_key,'format':'json','artist_location':country,'results':100,'start':the_start}
            try:
                get_artists_in_dict(parameters,dictionary)
                print 'created dict item for all the artists in this request'
            except:
                print 'sleeping for one minute, time now is:', datetime.now()
                time.sleep(60)
                get_artists_in_dict(parameters,dictionary)
                print 'created dict item for all the artists in this request'
                continue

def get_songs(the_artist_id,num_songs):
    # results = song.search(artist_id = the_artist_id,buckets=['audio_summary','song_hotttnesss'],results = num_songs)
    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key="+echonest_API_key+"&format=json&results="+str(num_songs)+"&artist_id="+the_artist_id+"&bucket=audio_summary&bucket=song_hotttnesss")
    r = r.json()
    return r

def create_empty_df():
    df_columns = ['country','artist_name','artist_id','song_name','song_id','song_hotness','energy','liveness','tempo','speechiness','acousticness','danceability',
    'instrumentalness','key','duration','loudness','audio_md5','valence','mode']
    df = pd.DataFrame(columns=df_columns)
    return df

def songs_to_df(country,songs,df):
    for song in songs:
        summary = song['audio_summary']
        df = df.append({'country':country,'artist_id':song['artist_id'],'artist_name':song['artist_name'],'song_name':song['title'],'song_id':song['id'],
            'song_hotness':song['song_hotttnesss'],'energy':summary['energy'],'liveness':summary['liveness'],
            'tempo':summary['tempo'],'speechiness':summary['speechiness'],'acousticness':summary['acousticness'],
            'danceability':summary['danceability'],'instrumentalness':summary['instrumentalness'],'key':summary['key'],
            'duration':summary['duration'],'loudness':summary['loudness'],
            'audio_md5':summary['audio_md5'],'valence':summary['valence'],'mode':summary['mode']},ignore_index=True)
    return df

# create artists dictionary by country, and get IDs
countries = ['lebanon','egypt','saudi arabia','united states','france','italy','nigeria','sudan','mali','morocco','mexico','china','japan','india','cuba']
artists_and_ids = defaultdict(list)
get_all_artists(countries,artists_and_ids,1000)
create_pickle(artists_and_ids,'all_artists.pkl')

# get 5 songs for each artist and put in pandas
artists_by_country = load_pickle('all_artists.pkl') 
used_countries = ['lebanon','egypt','united states','france','italy','nigeria','mexico','china','japan','india','cuba'] # 11 countries that have over 500 artists; these are the ones I will use
df = create_empty_df()

for country in used_countries:
    print 'starting country: ' + country
    artists = artists_by_country[country]
    for artist in artists:
        artistid = artist.keys()[0]
        artistname = artist.values()[0]
        try:
            the_songs_json = get_songs(artistid,5)
        except:
            print 'tried get_songs, sleeping, time now is:',datetime.now()
            time.sleep(60)
            the_songs_json = get_songs(artistid,5)
        
        try:
            the_songs = the_songs_json['response']['songs']
            df = songs_to_df(country,the_songs,df) 
        except:
            print 'tried the songs thing, sleeping, time now is:',datetime.now()
            time.sleep(60)
            the_songs_json = get_songs(artistid,5)
            the_songs = the_songs_json['response']['songs']
            df = songs_to_df(country,the_songs,df) 
        print 'so far length of df is ' + str(len(df)) + ' for artist ' + artistname + ' from country ' + country

print df
print len(df)
create_pickle(df,'all_songs.pkl')