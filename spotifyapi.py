import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPI:
    def __init__(self, id, secret):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=id,
                client_secret=secret,
            )
        )

    @staticmethod
    def get_artists_names(song):
        artists_names = []
        for artist in song["artists"]:
            artists_names.append(artist["name"])

        return artists_names

    @staticmethod
    def get_album_image(song):
        return song["album"]["images"][1]["url"]

    @staticmethod
    def get_preview(song):
        return song["preview_url"]

    def get_songs(self, songs):
        data = {}
        for song in songs:
            results = self.sp.search(
                q=song, type="track", market="US", limit=1
            )  # search song and artist
            song_data = results["tracks"]["items"][0]
            artists_names = self.get_artists_names(song_data)
            data[
                f"{song_data['name'].lower()} - {artists_names[0].lower()}"
            ] = song_data

        return data

    @staticmethod
    def get_popularity(songs_data):
        songs_popularity = {}
        for song, data in songs_data.items():
            songs_popularity[data["name"]] = data["popularity"]

        return songs_popularity
