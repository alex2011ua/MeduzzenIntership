from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel


from app.servises import dell_stop_words, sentiment_analysis, detect_language, read_item

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader("templates"))


class FormTextData(BaseModel):
    text: str


class FormAnalizedTextData(BaseModel):
    analyzed_text: list[dict]


@app.get("/")
def show_results(request: Request):
    """Displays a web interface to demonstrate a running application."""
    description = """
    Barack Obama gave a fantastic speech last night. Reports indicate he will move next to New Hampshire. Barack Obama wasn't the best president.
    Найкращим футболістом 2023 року за версією премії ФІФА The Best втретє став нападник "Інтер Маямі" та збірної Аргентини Ліонель Мессі, це новий рекорд.
    Мессі втретє виграв нагороду від ФІФА як найкращий футболіст року.
    """

    return templates.TemplateResponse("show_results.html", {"request": request, "description":description})


@app.post("/text_analyze")
async def text_analyze(data: FormTextData) -> list[dict]:
    # parce list of text for piece of texts with different languages
    list_of_text = data.text.split("\n")

    text_with_language_detect: list = []
    for item in list_of_text:
        text_with_language_detect.extend(detect_language(item))

    # lemmatization every part of text
    lemma_text: list = []
    for pair in text_with_language_detect:  # division into sentences and add language information
        a: dict = read_item((pair["language"], pair["text"]))
        for sentence in a["sentences"]:
            lemma_text.append(
                {"original_sentence": sentence["text"],
                 "language": pair["language"],
                 "code": pair["code"],
                 "tokens": sentence["tokens"],
                 }
            )
    # delete stop words
    lemma_text_without_stop_words = dell_stop_words(lemma_text)
    return lemma_text_without_stop_words

@app.post("/sentiment_analyze")
async def sentiment_analyze(data: FormAnalizedTextData) -> list[tuple]:
    sentences: list = []
    for sentence in data.analyzed_text:
        sentences.append(sentiment_analysis(sentence["original_sentence"], sentence["code"]))

    return sentences
