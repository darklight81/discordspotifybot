import discord
import os
import spotipy
from spotipy import SpotifyOAuth
from dotenv import load_dotenv
import validators

load_dotenv()
CLIENT_SECRET_DISC = os.getenv('CLIENT_SECRET_DISC')
SPOTIPY_CLIENT_ID = os.getenv('CLIENT_ID_SPOTIFY')
SPOTIPY_CLIENT_SECRET = os.getenv('CLIENT_SECRET_SPOTIFY')
SPOTIPY_REDIRECT_URI = os.getenv('REDIRECT_URI')
SPOTIFY_ID = 'lolskiller'
PLAYLIST_NAME = 'Test Playlist'

client = discord.Client()

scope = "user-library-read playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('--add'):
        if not validate_message(message):
            await message.channel.send('Wrong url.')
            return

        if not playlist_exists:
            sp.user_playlist_create(SPOTIFY_ID, PLAYLIST_NAME)
            print('test')


def validate_message(message):
    url = message.content
    url = url.split()[1]
    if not validators.url(url):
        return False
    return True


def playlist_exists():
    playlists = sp.user_playlists(SPOTIFY_ID)['items']
    exists = False
    for playlist in playlists:
        if playlist['name'] == PLAYLIST_NAME:
            exists = True
            break
    return exists


client.run(CLIENT_SECRET_DISC)
