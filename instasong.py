import cohere
import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

co = cohere.Client("COHERE_API_KEY")

client_id = "e1e49a36f77b48db9a29de85849ad181"
client_secret = "c542454ae4a5401f841eb65a0c696347"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)


# The front end code starts here
def get_artists_names(song):
    artists_names = []
    for artist in song["artists"]:
        artists_names.append(artist["name"])

    return artists_names


def get_album_image(song):
    return song["album"]["images"][1]["url"]


def get_preview(song):
    return song["preview_url"]


def get_songs(songs):
    data = {}
    for song in songs:
        results = sp.search(
            q=song, type="track", market="US", limit=1
        )  # search song and artist
        song_data = results["tracks"]["items"][0]
        artists_names = get_artists_names(song_data)
        data[f"{song_data['name'].lower()} - {artists_names[0].lower()}"] = song_data

    return data


def get_popularity(songs_data):
    songs_popularity = {}
    for song, song_data in songs_data.items():
        songs_popularity[songs_data[song]["name"]] = songs_data[song]["popularity"]

    return songs_popularity


st.title("InstaSong")
st.subheader("Get song suggestions for Instagram posts")
st.markdown("")  # filler

form = st.form(key="user_settings")
with form:
    # User input - Image URL and Post text
    image_url = st.text_input(
        "Image URL",
        key="image_url",
    )
    post_text = st.text_area(
        "Post Text",
        key="post_text",
    )

    submit_button = form.form_submit_button("Get Songs")

    if submit_button:
        if image_url == "":
            st.error("Image URL cannot be blank")
        else:
            # my_bar = st.progress(0.05)
            # Create a two-column view
            songs = {
                "golden harry styles",
                "flowers",
                "yellow",
            }  # array with searches to make (song name and artist name)

            songs_data = get_songs(songs)
            # get_popularity(songs_data)
            for song, data in songs_data.items():
                st.markdown("""---""")
                col1, col2 = st.columns([1, 2])
                with col1:
                    artists = get_artists_names(data)
                    display = f"<div style='display: flex; gap: 15px'><img src={get_album_image(data)} style='width: 64px; height: 64px; margin-left: 10px'><p><span style='font-size: large; font-weight: bold;'>{data['name']}</span><br>{artists[0]}</p></div>"
                    st.write(display, unsafe_allow_html=True)
                with col2:
                    st.audio(get_preview(data))
                # st.image(get_album_image(songs_data[song]))
                # st.markdown("##### " + songs_data[song]["name"])
                # st.write(artists[0])
                # my_bar.progress((i + 1) / 10)
            st.markdown("")  # filler
