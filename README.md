### Run Docker container
Go to the project directory

#### Activate docker
```bash
    docker-compose up
```

Web:
`GET /`
Displays a web interface to demonstrate a running application.
![img.png](img.png)

Endpoints:
`GET /text_analyze/`
parce list of text for piece of texts with different languages, lematize, and clear stop words.
```json
[
  {
    "original_sentence": "Barack Obama gave a fantastic speech last night.",
    "sentense_without_stopwords": "Barack Obama fantastic speech night .",
    "language": "english",
    "code": "en",
    "tokens": [
      {
        "id": 1,
        "text": "Barack",
        "dspan": [
          0,
          6
        ],
        "span": [
          0,
          6
        ],
        "lemma": "Barack"
      }, 
   ...

```
Endpoints:
`/sentiment_analyze`
Get JSON with text and return list of sentences with sentiment rating.



