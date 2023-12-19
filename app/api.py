import json

import pycld2 as cld2
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from forms import ShowResultsForm
from jinja2 import Environment, FileSystemLoader
from jinja2.runtime import Undefined
from trankit import Pipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader("templates"))


def dump_json(value: dict):
    """Pretty view json"""
    if isinstance(value, Undefined):  # to avoid exception in first open page without text
        return json.dumps({})
    return json.dumps(value, indent=2)


env.filters["to_nice_json"] = dump_json
templates.env = env

pipeline = Pipeline("english")
base_of_language = ["english"]


@app.get("/")
def show_results(request: Request):
    """Displays a web interface to demonstrate a running application."""
    return templates.TemplateResponse("show_results.html", {"request": request})


@app.post("/")
async def show_results(request: Request):
    """Displays a web interface to demonstrate a running application."""
    form = ShowResultsForm(request)
    await form.load_data()
    if form.is_valid():
        text_into_list: list = form.description.split("/n")
        answer = await text_analyze(text_into_list)
        pretty_json = json.dumps(answer)
        form.__dict__["pretty_json"] = pretty_json
    else:
        form.__dict__["pretty_json"] = {}
    return templates.TemplateResponse("show_results.html", form.__dict__)


@app.post("/text_analyze")
async def text_analyze(text: list[str]) -> list[list]:
    # parce list of text for piece of texts with different languages
    text_with_language_detect: list = []

    for item in text:
        text_with_language_detect.extend(detect_language(item))
    # lemmatization every part of text
    lemma_text: list = []
    for pair in text_with_language_detect:
        a: dict = await read_item((pair[0], pair[1]))
        pair.append(a["sentences"])
        lemma_text.append(pair)
    return lemma_text


@app.post("/lemmatization")
async def read_item(body: tuple[str, str]) -> dict:
    """
        Function to lemmatize the text
        it performs tokenization and sentence segmentation for the input document.
        Next, it assigns a lemma to each token in the sentences.

        :param body: body[0] is language, body[1] is text
        ["english", "Hello! This is Trankit."]
        :return:
       {
        "text": "Hello! This is Trankit.",
        "sentences": [
            {
                "id": 1,
                "text": "Hello!",
                "tokens": [
                    {
                        "id": 1,
                        "text": "Hello",
                        "dspan": [0,5],
                        "span": [0,5],
                        "lemma": "hello"
                    },
                    {
                        "id": 2,
                        "text": "!",
                        "dspan": [5,6],
                        "span": [5,6],
                        "lemma": "!"
                    }
                ],
                "dspan": [0,6]
            },
            {
                "id": 2,
                "text": "This is Trankit.",
                "tokens": [
                    {
                        "id": 1,
                        "text": "This",
                        "dspan": [7,11],
                        "span": [0,4],
                        "lemma": "this"
                    },
                   ...
            }
        ],
        "lang": "english"
    }
    """
    language, text = body[0], body[1]
    if language == "unknown":
        language = "english"
    if language not in base_of_language:
        pipeline.add(language)
        base_of_language.append(language)
    return pipeline.lemmatize(text)


def detect_language(text: str) -> list:
    """
    Function to detect language and position of change language
    :param text: Text to be analyzed
    :return: list of language and text
    """
    answer = []
    isReliable, textBytesFound, details, vectors = cld2.detect(text, returnVectors=True)
    for vector in vectors:
        answer.append([vector[2].lower(), text[vector[0] : vector[0] + vector[1]]])
    return answer


def parse_for_lemma(a: dict) -> list[str]:
    """
    parse big dict after trankit in little list with only lemmas
    :param a: dict
    :return: list
    """
    list_of_lemmas: list = []
    for sentence in a["sentences"]:
        for token in sentence["tokens"]:
            list_of_lemmas.append(token["lemma"])
    return list_of_lemmas
