import pandas as pd
import cohere
import numpy as np
import requests
from ast import literal_eval
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from sklearn.metrics.pairwise import cosine_similarity


class InstaSong:
    def __init__(self, dataset_name, cohere_api_key):
        self.co = cohere.Client(cohere_api_key)
        self.df = pd.read_csv(dataset_name, converters={"lyrics_embeds": literal_eval})

    def embed_text(self, texts):
        output = self.co.embed(model="embed-english-v2.0", texts=texts)
        embedding = output.embeddings

        return embedding

    def _get_similarity(self, target, candidates):
        # Turn list into array
        candidates = np.array(candidates)
        target = np.array(target)

        # Calculate cosine similarity
        sim = cosine_similarity(target, candidates)
        sim = np.squeeze(sim).tolist()

        # Sort by descending order in similarity
        sim = list(enumerate(sim))
        sim = sorted(sim, key=lambda x: x[1], reverse=True)

        # Return similarity scores
        return sim

    def process(self, img_url, text=""):
        processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        raw_image = Image.open(requests.get(img_url, stream=True).raw).convert("RGB")

        # unconditional image captioning
        inputs = processor(raw_image, return_tensors="pt")

        out = model.generate(**inputs)

        generated_text = processor.decode(out[0], skip_special_tokens=True)
        generated_text_embeds = self.embed_text([generated_text])
        # input_text_embeds = self.embed_text([text])

        # self.df["lyrics_embeds"] = embed_text(self.df["lyrics"].tolist())
        embeds = np.array(self.df["lyrics_embeds"].tolist())

        similarity = self._get_similarity(generated_text_embeds, embeds)
        # print(len(similarity))

        # top 10 similarity
        top_similarity = {}
        for idx, score in similarity[:10]:
            top_similarity[
                f"{self.df.iloc[idx]['song'].lower()} - {self.df.iloc[idx]['artist'].lower()}"
            ] = f"{score:.4f}"

        return top_similarity
