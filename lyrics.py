import configparser
import requests
from bs4 import BeautifulSoup


def getAccessToken():
  config = configparser.ConfigParser()
  config.read('config.ini')
  return config['Client_Access_Token']['token']

token = getAccessToken()

def searchMusicArtist(name):
  api_url = 'https://api.genius.com/search?q={}'.format(name)
  headers = {'Authorization': token}
  r = requests.get(api_url, headers=headers)
  return r.json()

def getArtistID(name):
  r = searchMusicArtist(name)
  id = r['response']['hits'][0]['result']['primary_artist']['id']
  return id

def getTopTenSongs(name):
  id = getArtistID(name)
  api_url = 'https://api.genius.com/artists/{}/songs'.format(id)
  headers = {'Authorization': token}
  params = {'sort': 'popularity', 'per_page': 10}
  r = requests.get(api_url, headers=headers, params=params)
  return r.json()

def getLyricsArray(name):
  songs = getTopTenSongs(name)
  lyrics = []
  for song in songs['response']['songs']:
    lyrics.append(song['url'])
  return lyrics

def scrapeLyricText(name):
  links = getLyricsArray(name)
  song_lyrics = []
  for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    lyrics_div = soup.find(class_='Lyrics__Container-sc-1ynbvzw-5 Dzxov')
    anchor_tags = lyrics_div.find_all('a')
    current_lyrics = []
    for anchor in anchor_tags:
      if anchor.text == '' or anchor.text[0] == '[':
        continue
      current_lyrics.append(anchor.get_text(separator=' NEWLINE '))
    song_lyrics.append(current_lyrics)
  return song_lyrics

