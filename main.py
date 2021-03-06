import os

import cv2
import pygame as pygame
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import time

import spotipy
import random
import requests
from bs4 import BeautifulSoup


pygame.mixer.init()

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()




username = 'Mohamed'
clientID = '86815c026a7041c591bcfd6576b96982'
clientSecret = 'd4bc149c382a48d4824ca34f56d71dba'
redirectURI = 'http://google.com/'
SCOPE='user-modify-playback-state'
oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI,state=None,scope=SCOPE)
token_dict = oauth_object.get_access_token()['access_token']
spotifyObject = spotipy.Spotify(auth=token_dict)
user = spotifyObject.current_user()
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def talk(text):
    engine.say(text)
    engine.runAndWait()

def rech (lists , item):
            p=True
            for list in lists :
               if(item['name'] ==list['name']) :
                   p=False
            return p
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source,3,4)
            print('recognition...')
            command = listener.recognize_google(voice)

            command = command.lower()
    except:
        command=""

    return command

def take_command1():
    try:
        with sr.Microphone() as source:

            voice = listener.listen(source,3,4)

            command = listener.recognize_google(voice)

            command = command.lower()
    except:
        command=""

    return command


def sleep():
    while True :
     command = take_command()
     if(command=='wake up'):
        talk('waking up')
        break



def run_alexa():
    command = take_command()
    print(command)
    if ("play " in command  ):
        song = command.replace('play ', '')
        talk('playing the song ' + song)
        searchQuery = song
        searchResults = spotifyObject.search(searchQuery, 1, 0, "track")
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        songs=[]
        songs.append(song)
        spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a',None,songs)
    elif 'next track' in command:
            talk('skipping to the next track')
            spotifyObject.next_track('6e46be61393591aba7f1275efdd2436463f1839a')
    elif 'pause' in command:
            spotifyObject.pause_playback('6e46be61393591aba7f1275efdd2436463f1839a')
    elif 'previous track' in command:
        talk('previous track')
        spotifyObject.previous_track('6e46be61393591aba7f1275efdd2436463f1839a')
    elif 'next song ' in command:
        song = command.replace('next song ', '')
        talk('adding to queue' + song)
        searchQuery = song
        searchResults = spotifyObject.search(searchQuery, 1, 0, "track")
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        spotifyObject.add_to_queue(song,'6e46be61393591aba7f1275efdd2436463f1839a')
    elif 'playlist' in command:
        song = command.replace('play', '')
        talk('playing the play list' + song)
        searchQuery = song
        searchResults = spotifyObject.search(searchQuery, 1, 0, "playlist")
        songs=[]
        tracks_dict = searchResults['playlists']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['id']
        results=spotifyObject.playlist(song)
        for item in results['tracks']['items']:
            music=item['track']
            songs.append(music['external_urls']['spotify'])
        spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a', None, songs)
    elif 'artist' in command:
        song = command.replace('artist', '')
        talk('playing ' + song)
        searchQuery = song
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
        tracks_dict = searchResults['artists']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        result=spotifyObject.artist_albums(song,album_type='album')
        albums=result['items']
        final_album=[]
        while result['next']:
            result=spotifyObject.next(result)
            albums.extend(result['items'])
        for album in albums :
              a=rech(final_album,album)
              if(a):
                final_album.append(album)
        randomsongs=[]
        s=0
        for album in final_album :
            tracks = spotifyObject.album_tracks(album['external_urls']['spotify'], 50, 0, None)
            tracks_items = tracks['items']
            s=s+len(tracks_items)
            if(s>50) :
                s=50
                break
        for i in range(0,s) :
            x = random.randint(0, len(final_album) - 1)
            album = final_album[x]['external_urls']['spotify']
            tracks = spotifyObject.album_tracks(album, 50, 0, None)
            tracks_items = tracks['items']
            y=random.randint(0,len(tracks)-1)
            randomsongs.append(tracks_items[y]['external_urls']['spotify'])
        spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a', None, randomsongs)
    elif 'album' in command:
        song = command.replace('album', '')
        talk('playing ' + song)
        searchQuery = song
        searchResults = spotifyObject.search(searchQuery, 1, 0, "album")
        tracks_dict = searchResults['albums']
        tracks_items = tracks_dict['items']
        album = tracks_items[0]['external_urls']['spotify']
        songs = []
        tracks = spotifyObject.album_tracks(album, 50, 0, None)
        tracks_items = tracks['items']
        i = 0
        while i != len(tracks_items):
            songs.append(tracks_items[i]['external_urls']['spotify'])
            i = i + 1
        spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a', None, songs)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is'  in command:
      try:
        person = command.replace('who is', '')
        info = wikipedia.summary(person,2,auto_suggest=False)
        print(info)
        talk(info)
      except :
         talk("cant find anything now" )
    elif 'what is'   in command:
      try:
        person = command.replace('what is', '')
        info = wikipedia.summary(person,2,auto_suggest=False)
        print(info)
        talk(info)
      except :
         talk("cant find anything now" )
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'security' in command:
        talk("activating security camera")
        os.system("python sec.py")
    elif 'news' in command:
        url = 'https://www.bbc.com/news'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find('body').find_all('h3')
        for x in headlines:
            talk(x.text.strip())
    elif 'stop' in command:
        talk("see you soon")
        quit()
    elif 'sleep' in command:
        talk("sleeping")
        sleep()
    elif 'hello' in command:
        talk("hello what can i do for you")
    else:
        talk('Please say the command again.')

cam = cv2.VideoCapture(0)
while True:
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        else :
         x, y, w, h = cv2.boundingRect(c)
         cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
         #winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
         talk("hello"+username+"welcome again")
         time.sleep(2)
         cam.release()
         while True :
          run_alexa()

