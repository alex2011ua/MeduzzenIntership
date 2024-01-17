from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from app.servises import remove_stop_words, detect_language, read_item, sentiment_analysis

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
Этот товар поражает своей невероятной функциональностью и стильным дизайном, добавляя радость и комфорт в повседневную жизнь. Высокое качество материалов и инновационные технологии делают этот товар идеальным выбором для тех, кто ценит комфорт и радость от использования. Этот товар не только отличается превосходным качеством, но и приносит непередаваемую радость своим удобством использования и стильным дизайном.
This product impresses with its incredible functionality and stylish design, adding joy and comfort to everyday life.The high-quality materials and innovative technologies make this product the perfect choice for those who value comfort and joy in usage.     This product not only stands out for its excellent quality but also brings unparalleled joy with its ease of use and stylish design.
Этот товар разочаровывает своей низкой надежностью и неудовлетворительным качеством материалов, что делает его приобретение невыгодным и неудовлетворительным опытом. Несмотря на обещания производителя, этот товар склонен к частым поломкам и не соответствует заявленным характеристикам, что вызывает негодование и разочарование у пользователей. Покупка этого товара оказалась ошибкой из-за его неэффективной работы и низкого качества исполнения, что вызывает недовольство и сожаление о потраченных средствах.
This product disappoints with its low reliability and unsatisfactory quality of materials, making its purchase unprofitable and providing a dissatisfying experience.  Despite the manufacturer's promises, this product is prone to frequent malfunctions and does not meet the claimed specifications, causing frustration and disappointment among users. Buying this product turned out to be a mistake due to its inefficient performance and low build quality, causing dissatisfaction and regret over the wasted money.
"""

    return templates.TemplateResponse(
        "show_results.html", {"request": request, "description": description}
    )


@app.post("/text_analyze")
async def text_analyze(data: FormTextData) -> list[dict]:
    """Endpoint for analyze the text and return json wit all text information."""
    # parce list of text for piece of texts with different languages
    list_of_text = data.text.split("\n")
    text_with_language_detect = sum([detect_language(text) for text in list_of_text], [])

    # lemmatization every part of text
    lemma_text: list = []
    for pair in text_with_language_detect:  # division into sentences and add language information
        a: dict = read_item((pair["language"], pair["text"]))
        for sentence in a["sentences"]:
            lemma_text.append(
                {
                    "original_sentence": sentence["text"],
                    "language": pair["language"],
                    "code": pair["code"],
                    "tokens": sentence["tokens"],
                }
            )
    # delete stop words
    lemma_text_without_stop_words = remove_stop_words(lemma_text)
    return lemma_text_without_stop_words


@app.post("/sentiment_analyze")
async def sentiment_analyze(data: FormAnalizedTextData) -> list[tuple[str | None, int | None]]:
    """Endpoint for sentiment analysis."""
    sentences: list = [sentiment_analysis(sentence["original_sentence"], sentence["code"]) for sentence in
                       data.analyzed_text]
    return sentences
