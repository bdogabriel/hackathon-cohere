### hackaton-cohere

# InstaSong
InstaSong is an application designed to be integrated with social networks to help users choose the perfect song for their posts.

## Use
The user inputs the image link for what will be posted and its caption, or just the image link, and InstaSong will suggest 10 songs that can best harmonize with the post.

## Behind the application
InstaSong can be thought as a combination of steps:

+ User input
+ Text generation from image with
+ Combination of the generated text and the optional caption: the **source text**
+ Embbeding between the **source text** and [our dataset](###-Our-dataset)
+ Extract the songs with the greatest similarity from the embedding and filter them to a minimum popularity
+ Display our results for the user

### Our dataset

## Prerequisites
To install all prerequisites, run
```
python3 dependencies.py
```

## Execute
To execute InstaSong, run
```
streamlit run app.py
```
Your application should be running on Port 8501