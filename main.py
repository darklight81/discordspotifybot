import discord
import export as export
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_SECRET_DISC = os.getenv('CLIENT_SECRET_DISC')
SPOTIPY_CLIENT_ID = os.getenv('CLIENT_ID_SPOTIFY')
SPOTIPY_CLIENT_SECRET = os.getenv('CLIENT_SECRET_SPOTIFY')
SPOTIPY_REDIRECT_URI = os.getenv('REDIRECT_URI')

client = discord.Client()

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('--add'):
        results = sp.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])
        await message.channel.send('Adding this to the playlist')

client.run(CLIENT_SECRET_DISC)
