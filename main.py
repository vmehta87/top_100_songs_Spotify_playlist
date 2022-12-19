from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time


date = input('What year do you want to travel to? Enter the date in the following format: YYYY-MM-DD ')

response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}/')
website = response.text
soup = BeautifulSoup(website, 'html.parser')

songs_h3 = soup.find_all(name='h3', id='title-of-a-story', class_="a-no-trucate")
song_list = [song.getText().strip('\t\n') for song in songs_h3]
print(song_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri="http://spotifysentiment.com/callback/",
        client_id='feac598c01ab4c1596647bd33e8dc472',
        client_secret='807b30df15fc4710938cec2261d9be25',
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_urls = []
year = date.split("-")[0]
failed = 0
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    time.sleep(.5)

    try:
        url = result["tracks"]["items"][0]["uri"]
        print(f'{song} ✔')
        song_urls.append(url)

    except IndexError:
        print(f'{song} not found in Spotify; **************Skipped')
        failed += 1

print(f'{failed} tracks were skipped')
playlist = sp.user_playlist_create(user=user_id, name=f'Top 100 tracks from {date}', public=True)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_urls)
