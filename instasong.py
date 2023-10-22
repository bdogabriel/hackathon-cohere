import cohere
import streamlit as st

co = cohere.Client("COHERE_API_KEY")

# The front end code starts here
st.title("Insta Song")
st.subheader("Get song suggestions for Instagram posts")

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
            my_bar = st.progress(0.05)
            for i in range(0, 10):
                st.markdown("""---""")
                st.markdown("##### " + "bagui")
                st.write("oi")
                my_bar.progress((i + 1) / 10)
