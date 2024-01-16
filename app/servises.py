import pycld2 as cld2
from polyglot.downloader import downloader
from polyglot.text import Text
from stopwordsiso import stopwords
from trankit import Pipeline

pipeline = Pipeline("english")
base_of_language = ["english"]

downloader.download("TASK:sentiment2", quiet=True)


def detect_language(text: str) -> list[dict]:
    """
    Function to detect language and position of change language.
    :param text: Text to be analyzed.
    :return: list of language and text.
    """
    answer = []
    _, _, _, vectors = cld2.detect(text, returnVectors=True)
    for vector in vectors:
        answer.append(
            {
                "language": vector[2].lower(),
                "text": text[vector[0] : vector[0] + vector[1]],
                "code": vector[3],
            }
        )
    return answer


def parse_for_lemma(a: dict) -> list[str]:
    """
    parse big dict after trankit in little list with only lemmas.
    :param a: dict.
    :return: list.
    """
    list_of_lemmas: list = []
    for sentence in a["sentences"]:
        for token in sentence["tokens"]:
            list_of_lemmas.append(token["lemma"])
    return list_of_lemmas


def dell_stop_words(lemma_text: list[dict]) -> list[dict]:
    """
    Deleting stopwords from lemmatized text.
    :param lemma_text: lemmatized text.
    :return: lemmatized text without stopwords.
    """
    lemma_text_without_stopwords = []
    for sentense in lemma_text:
        new_token = []
        words = []
        for token in sentense["tokens"]:
            if token["lemma"] in stopwords(sentense["code"]) or token[
                "text"
            ] in stopwords(sentense["code"]):
                continue
            new_token.append(token)
            words.append(token["lemma"])
        sentense_without_stopwords = " ".join(words)
        new_sentence = {
            "original_sentence": sentense["original_sentence"],
            "sentense_without_stopwords": sentense_without_stopwords,
            "language": sentense["language"],
            "code": sentense["code"],
            "tokens": new_token,
        }
        lemma_text_without_stopwords.append(new_sentence)

    return lemma_text_without_stopwords


def read_item(body: tuple[str, str]) -> dict:
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
    pipeline.set_active(language)
    return pipeline.lemmatize(text)


def sentiment_analysis(sentence: str, code: str) -> tuple:
    """
    Sentence Sentiment Analysis.
    :param sentence: str.
    :param code: str "en".
    :return: sentence and sentiment - counts of "good" or "bad" words:
        if sentiment > 0 : "good";
        if sentiment < 0 : "bad"
    """

    if code == "un":
        return None, None
    text = Text(sentence)
    try:
        sentiment = sum([word.polarity for word in text.words])
    except ValueError:
        return None, None
    return sentence, int(sentiment)
