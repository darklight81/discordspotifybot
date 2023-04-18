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
PLAYLIST_PREFIX = 'BaN - '

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)

scope = "user-library-read playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is a :bookmark: reaction
    if str(payload.emoji.name) == '🔖':
        channel = await client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        playlist_name = PLAYLIST_PREFIX + str(message.channel)
        if not message.content.startswith('https://open.spotify.com/'):
            await message.add_reaction('👎')
            return
        track_id = validate_message(message)
        if not track_id:
            await message.add_reaction('👎')
            return
        playlist_id = playlist_exists(playlist_name)
        if not playlist_id:
            sp.user_playlist_create(SPOTIFY_ID, playlist_name)
            playlist_id = playlist_exists(playlist_name)
        try:
            sp.playlist_add_items(playlist_id, {track_id})
        except:
            await message.add_reaction('👎')
            return

        track = sp.track(track_id)
        await message.add_reaction('👌')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!gn'):
        emoji = discord.utils.get(client.emojis, name='moyalSleep')
        if emoji:
            await message.channel.send(str(emoji))


# Validates the message sent by client and returns track id or false
def validate_message(message):
    url = message.content
    url = url.split()[0]
    print('url: ', url)
    if not validators.url(url):
        return False

    split_url = url.split('/')
    track_id = False

    for id_el, el in enumerate(split_url):
        if el == 'track':
            try:
                track_id = split_url[id_el + 1]
            except IndexError:
                return False
            break

    if not track_id:
        return False

    track_id = track_id.split('?')[0]
    try:
        sp.track(track_id)
    except:
        return False

    return track_id


# Checks the existence of playlist, if doesnt exist, returns false,  else returns playlist id
def playlist_exists(playlist_name):
    playlists = sp.user_playlists(SPOTIFY_ID)['items']
    playlist_id = False
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    return playlist_id


if __name__ == '__main__':
    client.run(CLIENT_SECRET_DISC)