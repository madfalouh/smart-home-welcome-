import cv2
import winsound
import time
import speech_recognition as sr
import pyttsx3
#import pywhatkit
import datetime
import wikipedia
import pyjokes
import json
import spotipy
import webbrowser
import random
username = 'Mohamed'
clientID = '86815c026a7041c591bcfd6576b96982'
clientSecret = 'd4bc149c382a48d4824ca34f56d71dba'
redirectURI = 'http://google.com/'
oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
token_dict = oauth_object.get_access_token()
token = 'BQDvzNsZ3u7KPwlQnt1061lnU5oPtQ260INr05jLtkragMVopbezCcKtLUod1jGCcN7Z624PJn3rPMbDpyMmH6dClKm0Qb3GxFl2lq_hOChPg5ZF_mg2HfpGORTbqz3PuwTTX5uYfLMfiuFlaR5A7267KtLmR6tmvz0jU_DA_m1n7LBMu9ObSo_bDUYXTDohLVTOhntz9OKNiyvza2SN_asvhyg3w-ri6u3fw9Okat4-Io6LqQ'
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
#print(json.dumps(user,sort_keys=True, indent=4))
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
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command.replace('alexa', '')

    except:
        print("there is an error")

    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        searchQuery = song
        searchResults = spotifyObject.search(searchQuery, 1, 0, "track")
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        songs=[]
        songs.append(song)
        #spotifyObject.next_track('6e46be61393591aba7f1275efdd2436463f1839a')
        spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a',None,songs)
    if 'next track' in command:

            talk('skiping to the nexte track')
            # spotifyObject.next_track('6e46be61393591aba7f1275efdd2436463f1839a')
            spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a', None, songs)
    if 'pause' in command:
            # spotifyObject.next_track('6e46be61393591aba7f1275efdd2436463f1839a')
            spotifyObject.pause_playback('6e46be61393591aba7f1275efdd2436463f1839a')
    if 'artist' in command:
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
        randomsong=[]
        n=len(final_album)

        for i in range(0,50) :
            x = random.randint(0, len(final_album) - 1)
            album = final_album[x]['external_urls']['spotify']
            tracks = spotifyObject.album_tracks(album, 50, 0, None)
            tracks_items = tracks['items']
            y=random.randint(0,len(tracks)-1)
            randomsongs.append(tracks_items[y]['external_urls']['spotify'])
        spotifyObject.start_playback('6e46be61393591aba7f1275efdd2436463f1839a', None, randomsongs)

    if 'album' in command:
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
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
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
         #time.sleep(19)
         while True :
          run_alexa()

