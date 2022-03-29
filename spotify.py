# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:47:18 2020

@author: andrew
"""

import spotipy
import pandas as pd
import time, requests, base64, sys, os
import cred 
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
###https://github.com/plamere/spotipy/tree/master/examples
###https://developer.spotify.com/documentation/web-api/reference/#/
###https://developer.spotify.com/documentation/general/guides/authorization/



#spotify web api

redirect_uri = 'http://localhost:8889/callback/'
scope = "user-library-read playlist-read-collaborative playlist-read-private playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id,
                                               client_secret=cred.client_secret,
                                               redirect_uri=redirect_uri, scope=scope))
 
results = sp.user_playlists(cred.user_id)

playlist_id = None
 

playlist_details = []

for i in results['items']:
    name = i['name']
    ids = i['id']
    playlist_details.append([name,ids])


def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

def getTrackFeatures(id):
  meta = sp.track(id)
  features = sp.audio_features(id)

  # meta
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']

  # features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']

  track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
  return track


ids = getTrackIDs(cred.user_id, '3cEQcPotnho81A9sBSZyJG')

def track_identify(ids):
    tracks = []
    for i in range(len(ids)):
      time.sleep(.5)
      track = getTrackFeatures(ids[i])
      tracks.append(track)
    return tracks

track_ids = track_identify(ids)

#'Andrew API Playlist', '3cEQcPotnho81A9sBSZyJG'

song_list = pd.read_csv(r"C:\Python\spotify\shazamlibrary.csv")

song_names = song_list[['Title','Artist']]
song_names = song_names.to_numpy()

def spotify_song_check(songs):
    song_details = []
    track_ids_list = []
    for song in songs:
        song_name = str(song[0])
        artist_name = str(song[1])
        searchResults = sp.search(q="artist:" + artist_name + " track:" + song_name, type="track")
        
        for x in searchResults['tracks']['items'][:1]:
            name = x['name']
            artist = x['artists'][0]['name']
            artist_uri = x['artists'][0]['uri']
            album = x['album']['artists'][0]['name']
            song_id = x['id']
            uri = x['uri']
            song_details.append([name, artist,artist_uri, album,song_id,uri])
            track_ids_list.append(song_id)

    return song_details, track_ids_list


songs = spotify_song_check(song_names)

shazam_id = '09io9OdgOrojkRMndXTW8n'
shazam_uri = "spotify:playlist:09io9OdgOrojkRMndXTW8n"

shazam_ids = getTrackIDs(cred.user_id, shazam_id)
shazam_songs = track_identify(shazam_ids)

def track_checker(song_list,playlist_list):
    new_list = []
    for song in song_list:
        if song not in playlist_list:
            new_list.append(song)
    return new_list
            
check_songs = track_checker(songs[1],shazam_ids)
            

# create dataset
shazam_df = pd.DataFrame(shazam_songs , columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
#shazam_df.to_csv("spotify.csv", sep = ',')
current_songs_in_shazam = shazam_df[['name','artist']]
current_songs_in_shazam = current_songs_in_shazam.to_numpy()

def add_songs_playlist(playlist,songs):
    if not songs:
        print("No Songs to add to playlist")
    else:
        sp.playlist_add_items(playlist, songs)

add_songs_playlist(shazam_id,check_songs)

