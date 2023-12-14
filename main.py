from fastapi import FastAPI
from langdetect import detect_langs
from trankit import Pipeline

app = FastAPI()


@app.post("/text")
async def read_item(text: list[str]):
    lang = detect_langs(text[0])
    return lang


@app.post("/segmentation")
async def read_item(text: list[str]):
    p = Pipeline('english')
    sentences = p.lemmatize(text[0])
    return sentences
