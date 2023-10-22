import streamlit as st
import instasong
import spotifyapi

# The front end code starts here

sfapi = spotifyapi.SpotifyAPI(
    st.secrets["SPOTIFY_CLIENT_ID"], st.secrets["SPOTIFY_CLIENT_SECRET"]
)
isong = instasong.InstaSong("dataframe_pop.csv", st.secrets["COHERE_API_KEY"])

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
            songs = isong.process_image(image_url)

            print(songs)

            songs_data = sfapi.get_songs(songs.keys())

            # get_popularity(songs_data)
            for song, data in songs_data.items():
                st.markdown("""---""")
                col1, col2 = st.columns([1, 2])
                with col1:
                    artists = spotifyapi.SpotifyAPI.get_artists_names(data)
                    display = f"<div style='display: flex; gap: 15px'><img src={spotifyapi.SpotifyAPI.get_album_image(data)} style='width: 64px; height: 64px; margin-left: 10px'><p><span style='font-size: large; font-weight: bold;'>{data['name']}</span><br>{artists[0]}</p></div>"
                    st.write(display, unsafe_allow_html=True)
                with col2:
                    st.audio(spotifyapi.SpotifyAPI.get_preview(data))
                # st.image(get_album_image(songs_data[song]))
                # st.markdown("##### " + songs_data[song]["name"])
                # st.write(artists[0])
                # my_bar.progress((i + 1) / 10)
            st.markdown("")  # filler
