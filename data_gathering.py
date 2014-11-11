# Dara Elass

from auth_ids import echonest_API_key, spotify_API_key
from pyechonest import song
from pyechonest import artist
from pyechonest import config
import musixmatch
import urllib2
from bs4 import BeautifulSoup
import pickle
import re
import time
from datetime import datetime
import json

######################################################################################
# # general functions
######################################################################################

def create_pickle(data):
    file_name = str(data)+'.pkl'
    with open(file_name,'w') as picklefile:
        pickle.dump(data,picklefile)

def load_pickle(filename):
    data_name = filename[:-4]
    print data_name
    with open(filename,'r') as picklefile:
        data_name = pickle.load(picklefile)
    return data_name

######################################################################################
# # webscraping lyricstranslate.com for all Arabic -> English lyrics
######################################################################################

# # connect using beautiful soup
# def connect(url):
#     page = urllib2.urlopen(url)
#     return BeautifulSoup(page.read(), 'html5lib')

# # get urls of all pages
# def get_page_urls(num_pages):
#     translations_url_first = "http://lyricstranslate.com/en/translations/12/328/none/none/none"
#     translations_url_others = "http://lyricstranslate.com/en/translations/12/328/none/none/none-page-"
#     all_page_urls = [translations_url_first]
#     for i in range(num_pages-1): 
#         all_page_urls.append(translations_url_others+str(i+1))
#     return all_page_urls

# # get urls of each translation
# def get_all_lyrics_urls(page_urls):
#     lyrics_urls = []
#     for page_url in page_urls:
#         page_soup = connect(page_url)
#         for row in page_soup.findAll('tr')[1:]:
#             column = row.findAll('td',{'class':'ltsearch-translatenameoriginal'})[1]
#             url = column.find('a', href = re.compile("/en/"))  
#             link = "http://lyricstranslate.com"+url['href']
#             lyrics_urls.append(link)
#     return lyrics_urls

# # get artist name from translation
# def get_artist(lyric_url):
#     lyrics_soup = connect(lyric_url)
#     artist = lyrics_soup.find('li',{'class':'song-node-info-artist'}).a.text
#     return artist

# # get song name in original language (sometimes this is transliterated)
# def get_song(lyric_url):
#     lyrics_soup = connect(lyric_url)
#     song = lyrics_soup.find('div',{'class':'song-node-text'}).find('h2').text
#     return song

# # get name of song, translated
# def get_english_title(lyric_url):
#     lyrics_soup = connect(lyric_url)
#     song = lyrics_soup.find('div',{'class':'translate-node-text '}).find('h2').text
#     return song

# # get english lyrics
# def get_english_translation(lyric_url):
#     lyrics_soup = connect(lyric_url)
#     paragraphs = lyrics_soup.find('div',{'class':'translate-node-text '}).h2.findNextSiblings('p')
#     lyrics = []
#     for paragraph in paragraphs:
#         paragraph = paragraph.text.splitlines()
#         lyrics.extend(paragraph)
#     return lyrics

# # create lyrics_urls pickle file to use moving forward:
# num_pages = 39
# all_page_urls = get_page_urls(num_pages)
# print 'got page urls'
# lyrics_urls = get_all_lyrics_urls(all_page_urls)
# print 'got lyrics urls'
# with open('lyrics_urls.pkl', 'w') as picklefile:
#     pickle.dump(lyrics_urls, picklefile)

# # create dictionary with all the lyrics and pickle file
# with open('lyrics_urls.pkl', 'r') as picklefile: 
#     lyrics_urls = pickle.load(picklefile)
# all_arabic_songs = {}
# for i,url in enumerate(lyrics_urls):
#     print 'started number',i
#     try:
#         artist = get_artist(url)
#     except:
#         print i, 'problem with artist:', url
#         break
#     try:
#         song = get_song(url)
#     except:
#         print i, 'problem with song:',url
#         break
#     try:
#         english_song = get_english_title(url)
#     except:
#         print i, 'problem with english title:',url
#         lyrics_soup = connect(url)
#         english_song = lyrics_soup.find('div',{'class':'translate-node-text translate-node-text-proofreading'}).find('h2').text
#     try:
#         lyrics = get_english_translation(url)
#     except:
#         print i, 'problem with lyrics:',url
#         lyrics_soup = connect(url)
#         paragraphs = lyrics_soup.find('div',{'class':'translate-node-text translate-node-text-proofreading'}).h2.findNextSiblings('p')
#         lyrics = []
#         for paragraph in paragraphs:
#             paragraph = paragraph.text.splitlines()
#             lyrics.extend(paragraph)
#     try:
#         all_arabic_songs[(artist,song,english_song)]=lyrics
#     except:
#         print i, 'problem with dictionary'
#         break
# with open('all_arabic_songs.pkl','w') as picklefile:
#     pickle.dump(all_arabic_songs,picklefile)

# # test new pickle file
# with open('all_arabic_songs.pkl','r') as picklefile:
#     all_arabic_songs = pickle.load(picklefile)

######################################################################################
# # getting popular artists and five of their songs from echonest 
######################################################################################

config.ECHO_NEST_API_KEY = echonest_API_key

# # get 1000 top artists accoridng to echonest's "hotttnesss" features
# top_artists = {}
# for the_artist in artist.top_hottt(results = 1000):
#     try:
#         name = the_artist.name
#         hotness = the_artist.hotttnesss
#         ID = the_artist.id
#         top_artists[(name,ID)] = hotness
#         print name, hotness
#     except:
#         print 'waiting one minute'
#         print 'time now is:', datetime.now()
#         time.sleep(60)
#         continue

# with open('top_1000_artists_english.pkl','w') as picklefile:
#     pickle.dump(top_artists,picklefile)

# # get 5 most popular song names from each of the artists
# with open('top_1000_artists_english.pkl','r') as picklefile:
#     top_artists = pickle.load(picklefile)

# artists_and_songs = {} # key = artist, value = song name
# artists_and_songs_ids = {} # key = artist, value = song id
# for k in top_artists.keys():
#     the_artist = k[0]
#     artist_id = k[1]
#     try:
#         songs = artist.Artist(the_artist).get_songs(results=5)
#         artist_songs = []
#         song_ids = []
#         for song in songs[:5]:
#             artist_songs.append(song)
#             song_ids.append(song.id)
#         artists_and_songs[the_artist] = artist_songs
#         artists_and_songs_ids[the_artist] = song_ids
#         print the_artist, ':', artist_songs
#     except:
#         print 'waiting one minute'
#         print 'time now is:', datetime.now()
#         time.sleep(60)

# create_pickle(artists_and_songs)
# create_pickle(artists_and_songs_ids)

######################################################################################
# # getting lyrics of the songs from lyricfind/echonest
######################################################################################
    
# # get lyrics of the ~5000 songs using lyricfind's api
# artists_and_songs = load_pickle('artists_and_songs.pkl')
# artists_and_songs_id = load_pickle('artists_and_songs_id.pkl')

def get_lyrics(song):
    lyricfind_id = song.get_foreign_id('lyricfind-US').replace('lyricfind-US:song:', '')
    url = 'http://test.lyricfind.com/api_service/lyric.do?apikey='+lyricfind_api_key+'&reqtype=default&trackid=elid:'+lyricfind_id
    open_url = urllib.urlopen(url)
    js = open_url.read()
    open_url.close()
    dict_lyrics = json.loads(js)
    try:
        lyrics = dict_lyrics['track']['lyrics']
        for line in lyrics.split('\r\n'):
            print line
        print
    except:
        print '(no lyrics)'

######################################################################################
# # find arabic songs in echonest or spotify
######################################################################################
