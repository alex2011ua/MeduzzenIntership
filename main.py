from fastapi import FastAPI
from trankit import Pipeline
import pycld2 as cld2

app = FastAPI()
pipeline = Pipeline("english")
base_of_language = ["english"]


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
        lemma_text.append(parse_for_lemma(a))
    return lemma_text


@app.post("/lemmatization")
async def read_item(body: tuple[str, str]) -> dict:
    """
    Function to lemmatize the text
    it performs tokenization and sentence segmentation for the input document.
    Next, it assigns a lemma to each token in the sentences.

    :param body: body[0] is language, body[1] is text
    :return:
    {
   'text': 'Hello! This is Trankit.',  # input string
   'sentences': [ # list of sentences
    {
      'id': 1, 'text': 'Hello!', 'dspan': (0, 6), 'tokens': [...]
    },
    {
      'id': 2,  # sentence index
      'text': 'This is Trankit.',  'dspan': (7, 23), # sentence span
      'tokens': [ # list of tokens
        {
          'id': 1, # token index
          'text': 'This',
          'lemma': 'this', # lemma of the token
          'dspan': (7, 11), # document-level span of the token
          'span': (0, 4) # sentence-level span of the token
        },
        {'id': 2...},
        {'id': 3...},
        {'id': 4...}
      ]
    }
    ]
    }
    """
    language, text = body[0], body[1]
    if language == 'unknown':
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
        answer.append(
            [
                vector[2].lower(), text[vector[0]: vector[0] + vector[1]]
            ]
        )
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
