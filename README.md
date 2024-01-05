### Run Docker container
Go to the project directory

#### Activate docker
```bash
    docker-compose up
```

Endpoints:
`GET /`
Displays a web interface to demonstrate a running application.

`GET /shop/items/`
parce list of text for piece of texts with different languages
```json
[
    [
        "english",
        "France is the largest country in Western Europe and the third-largest in Europe as a whole.",
        [
            {
                "id": 1,
                "text": "France is the largest country in Western Europe and the third-largest in Europe as a whole.",
                "tokens": [
                    {
                        "id": 1,
                        "text": "France",
                        "dspan": [
                            0,
                            6
                        ],
                        "span": [
                            0,
                            6
                        ],
                        "lemma": "France"
                    },
                    {
                        "id": 19,
                        "text": ".",
                        "dspan": [
                            90,
                            91
                        ],
                        "span": [
                            90,
                            91
                        ],
                        "lemma": "."
                    }
                ],
                "dspan": [
                    0,
                    91
                ]
            }
        ]
    ]
]


`/lemmatization`

return dict of sentence, tokens, lemmas, languages



