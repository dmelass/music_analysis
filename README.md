Passion Project: Music Analysis
==============

This is my final project at my data science bootcamp at Metis. In this project I will analyze musical elements of songs from 11 countries (Lebanon, Egypt, United States, France, Italy, Nigeria, Mexico, China, Japan, India, Cuba) using metadata gathered from echonest's API.

<b>In this respository...</b>

data_gathering.py - this script collects 500+ artist names from the chosen countries, and then gathers 5 songs per artist and puts all the song metadata in a pandas dataframe. I collected metadata for about 40,000 songs.

data_analysis.py - this script uses DBSCAN to create clusters of the songs using the following features: energy, liveness, tempo, speechiness, acousticness, danceability, instrumentalness, duration, loudness, valence, key, and mode.