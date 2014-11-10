# Dara Elass

from pyechonest import config
from pyechonest import artist
from pyechonest import song
from auth_ids import echonest_API_key, spotify_API_key
import spotipy
import musixmatch
import urllib2
from bs4 import BeautifulSoup
import pickle
import re

######################################################################################
# webscraping lyricstranslate.com for all Arabic -> English lyrics
######################################################################################

# connect using beautiful soup
def connect(url):
    page = urllib2.urlopen(url)
    return BeautifulSoup(page.read(), 'html5lib')

# get urls of all pages
def get_page_urls(num_pages):
    translations_url_first = "http://lyricstranslate.com/en/translations/12/328/none/none/none"
    translations_url_others = "http://lyricstranslate.com/en/translations/12/328/none/none/none-page-"
    all_page_urls = [translations_url_first]
    for i in range(num_pages-1): 
        all_page_urls.append(translations_url_others+str(i+1))
    return all_page_urls

# get urls of each translation
def get_all_lyrics_urls(page_urls):
    lyrics_urls = []
    for page_url in page_urls:
        page_soup = connect(page_url)
        for row in page_soup.findAll('tr')[1:]:
            column = row.findAll('td',{'class':'ltsearch-translatenameoriginal'})[1]
            url = column.find('a', href = re.compile("/en/"))  
            link = "http://lyricstranslate.com"+url['href']
            lyrics_urls.append(link)
    return lyrics_urls

# get artist name from translation
def get_artist(lyric_url):
    lyrics_soup = connect(lyric_url)
    artist = lyrics_soup.find('li',{'class':'song-node-info-artist'}).a.text
    return artist

def get_song(lyric_url):
    lyrics_soup = connect(lyric_url)
    song = lyrics_soup.find('div',{'class':'song-node-text'}).find('h2').text
    return song

def get_english_title(lyric_url):
    lyrics_soup = connect(lyric_url)
    song = lyrics_soup.find('div',{'class':'translate-node-text '}).find('h2').text
    return song

def get_english_translation(lyric_url):
    lyrics_soup = connect(lyric_url)
    paragraphs = lyrics_soup.find('div',{'class':'translate-node-text '}).h2.findNextSiblings('p')
    lyrics = []
    for paragraph in paragraphs:
        paragraph = paragraph.text.splitlines()
        lyrics.extend(paragraph)
    return lyrics

# run script

# create lyrics_urls pickle file to use moving forward:
    # num_pages = 39
    # all_page_urls = get_page_urls(num_pages)
    # print 'got page urls'
    # lyrics_urls = get_all_lyrics_urls(all_page_urls)
    # print 'got lyrics urls'
    # with open('lyrics_urls.pkl', 'w') as picklefile:
    #     pickle.dump(lyrics_urls, picklefile)

if __name__ == '__main__':
    with open('lyrics_urls.pkl', 'r') as picklefile: 
        lyrics_urls = pickle.load(picklefile)
    all_arabic_songs = {}
    for i,url in enumerate(lyrics_urls):
        print 'started number',i
        try:
            artist = get_artist(url)
        except:
            print i, 'problem with artist:', url
            break
        try:
            song = get_song(url)
        except:
            print i, 'problem with song:',url
            break
        try:
            english_song = get_english_title(url)
        except:
            print i, 'problem with english title:',url
            lyrics_soup = connect(url)
            english_song = lyrics_soup.find('div',{'class':'translate-node-text translate-node-text-proofreading'}).find('h2').text
        try:
            lyrics = get_english_translation(url)
        except:
            print i, 'problem with lyrics:',url
            lyrics_soup = connect(url)
            paragraphs = lyrics_soup.find('div',{'class':'translate-node-text translate-node-text-proofreading'}).h2.findNextSiblings('p')
            lyrics = []
            for paragraph in paragraphs:
                paragraph = paragraph.text.splitlines()
                lyrics.extend(paragraph)
        try:
            all_arabic_songs[(artist,song,english_song)]=lyrics
        except:
            print i, 'problem with dictionary'
            break
    with open('all_arabic_songs.pkl','w') as picklefile:
        pickle.dump(all_arabic_songs,picklefile)
