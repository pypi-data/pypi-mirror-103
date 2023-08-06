# tldr-python

Python wrapper for the TLDR text summarization and analysis API available on [RapidAPI](https://rapidapi.com/AmolMavuduru/api/tldr-text-analysis).

## Installation

```
pip install tldr-python
```

## Introduction - Getting Started

tldr-python is a wrapper over the TLDR text summarization and analysis API. To use this API, create an account on [RapidAPI](https://rapidapi.com/) and [subscribe to the API](https://rapidapi.com/AmolMavuduru/api/tldr-text-analysis).

Once you have a RapidAPI key, initialize a TLDR instance as demonstrated below.

```
from tldr_python import TLDR
tldr = TLDR('<your RapidAPI key>')
```

## Text Summarization

You can use TLDR to summarize articles on the web with the **summarize** function. This function accepts either a URL or the raw text of an article on the web. 

We can summarize a Wikipedia article about Python using the code below.

```
summary = tldr.summarize('https://en.wikipedia.org/wiki/Python_(programming_language)', max_sentences=3)
print(summary.text)
```

The code above produces the following summary:

```
'[34][35][36][37][38] History[edit] Python was conceived in the late 1980s[39] by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands as a successor to ABC programming language, which was inspired by SETL,[40] capable of exception handling and interfacing with the Amoeba operating system.[67] The standard library has two modules (itertools and functools) that implement functional tools borrowed from Haskell and Standard ML.[69] Alex Martelli, a Fellow at the Python Software Foundation and Python book author, writes that "To describe something as \'clever\' is not considered a compliment in the Python culture.'
```

## Keyword Extraction

We can also extract keywords from an article as shown below.

```
keywords = tldr.extract_keywords('https://en.wikipedia.org/wiki/Python_(programming_language)', n_keywords=3)
print(keywords.json)
```

The result of the code above is a JSON list with the top three scored keywords from the article.

```
[{'keyword': 'python', 'score': 402}, {'keyword': 'language', 'score': 68}, {'keyword': 'software', 'score': 47}]
```

## Sentiment Analysis

We can also analyze the sentiment of an article with the **analyze_sentiment function**. This function returns a Sentiment object with sentiment and polarity attributes.

```
sentiment = tldr.analyze_sentiment('https://en.wikipedia.org/wiki/Python_(programming_language)')
print(sentiment.json)
```

The code above gives a dictionary with the sentiment and polarity of the article.

```
{'sentiment': 'positive', 'polarity': 0.10235096701177092}
```
