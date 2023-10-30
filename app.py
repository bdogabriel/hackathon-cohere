import streamlit as st
import instasong
import spotifyapi

import operator
from collections import OrderedDict


def sort_dict(dict1):
    sorted_tuples = sorted(dict1.items(), key=operator.itemgetter(1), reverse=True)

    sorted_dict = OrderedDict()
    for k, v in sorted_tuples:
        sorted_dict[k] = v

    return sorted_dict


sfapi = spotifyapi.SpotifyAPI(
    st.secrets["SPOTIFY_CLIENT_ID"], st.secrets["SPOTIFY_CLIENT_SECRET"]
)
isong = instasong.InstaSong("./dataframes/data.csv", st.secrets["COHERE_API_KEY"])

st.title(":rainbow[InstaSong]")
st.subheader("Get song suggestions for Instagram posts")
st.markdown("")  # filler

form = st.form(key="user_settings")
with form:
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
            st.write(
                f"<img src={image_url} style='height: 250px'; display: block; margin-left: auto; margin-right:auto>",
                unsafe_allow_html=True,
            )
            songs = sort_dict(isong.process(image_url, post_text))
            songs_data = sfapi.get_songs(songs.keys())

            for song, data in songs_data.items():
                st.markdown("""---""")
                col1, col2 = st.columns([1, 2])
                with col1:
                    artists = spotifyapi.SpotifyAPI.get_artists_names(data)
                    display = f"<div style='display: flex; gap: 15px'><img src={spotifyapi.SpotifyAPI.get_album_image(data)} style='width: 64px; height: 64px; margin-left: 10px'><p><span style='font-size: large; font-weight: bold;'>{data['name']}</span><br>{artists[0]}</p></div>"
                    st.write(display, unsafe_allow_html=True)
                with col2:
                    st.audio(spotifyapi.SpotifyAPI.get_preview(data))
            st.markdown("")  # filler
