### Run Docker container
Go to the project directory

#### Activate docker
```bash
    docker-compose up
```


So the general topics in text:

1. Cleaning

We have powerfool build in functions in Python like str.maketrans('', '', string.punctuation), str.replace(""", " ") or 
library re to clean and delete unimportant information

2. Language detection
pycld2

langdetect supports 55 languages out of the box and this list can be added 

4. convert a string containing human language text into lists of sentences and words
trankit better
Using spaCy library, we can convert string to list with detect parts of speech and morphological features

5. generate base forms of those words

we can use spaCy to make base forms ( [token.lemma_ for token in doc] )

6. detect parts of speech and morphological features

6. dependency parsing

spaCy features a fast and accurate syntactic dependency parser, and has a rich API for navigating the tree. 
7. Provide syntactic structure
8. recognize named entities
9. 30+ languages
10. have fun...


General topics in email classification and extraction:
1. Again 30+ languages
2. Diff between Categorization and classification

Categorization is a creative synthesis based on context or perceived similarity

3. Features to use

Email is also a text. So we can use the same features as SpaCy

4. Different approaches

5. Input segmentation (find the 'real' content esp. in emails

we can omit the greeting and farewell parts of the letter

6. email formats: txt, eml, msg
7. Extraction of information, general and specific ones
8. Start loving language problems 😊

![img_3.png](img_3.png)