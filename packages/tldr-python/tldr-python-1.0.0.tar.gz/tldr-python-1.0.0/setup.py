# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tldr_python']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.5,<3.0']

setup_kwargs = {
    'name': 'tldr-python',
    'version': '1.0.0',
    'description': 'Python wrapper for the TLDR text summarization and analysis API.',
    'long_description': '# tldr-python\n\nPython wrapper for the TLDR text summarization and analysis API available on [RapidAPI](https://rapidapi.com/AmolMavuduru/api/tldr-text-analysis).\n\n## Installation\n\n```\npip install tldr-python\n```\n\n## Introduction - Getting Started\n\ntldr-python is a wrapper over the TLDR text summarization and analysis API. To use this API, create an account on [RapidAPI](https://rapidapi.com/) and [subscribe to the API](https://rapidapi.com/AmolMavuduru/api/tldr-text-analysis).\n\nOnce you have a RapidAPI key, initialize a TLDR instance as demonstrated below.\n\n```\nfrom tldr_python import TLDR\ntldr = TLDR(\'<your RapidAPI key>\')\n```\n\n## Text Summarization\n\nYou can use TLDR to summarize articles on the web with the **summarize** function. This function accepts either a URL or the raw text of an article on the web. \n\nWe can summarize a Wikipedia article about Python using the code below.\n\n```\nsummary = tldr.summarize(\'https://en.wikipedia.org/wiki/Python_(programming_language)\', max_sentences=3)\nprint(summary.text)\n```\n\nThe code above produces the following summary:\n\n```\n\'[34][35][36][37][38] History[edit] Python was conceived in the late 1980s[39] by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands as a successor to ABC programming language, which was inspired by SETL,[40] capable of exception handling and interfacing with the Amoeba operating system.[67] The standard library has two modules (itertools and functools) that implement functional tools borrowed from Haskell and Standard ML.[69] Alex Martelli, a Fellow at the Python Software Foundation and Python book author, writes that "To describe something as \\\'clever\\\' is not considered a compliment in the Python culture.\'\n```\n\n## Keyword Extraction\n\nWe can also extract keywords from an article as shown below.\n\n```\nkeywords = tldr.extract_keywords(\'https://en.wikipedia.org/wiki/Python_(programming_language)\', n_keywords=3)\nprint(keywords.json)\n```\n\nThe result of the code above is a JSON list with the top three scored keywords from the article.\n\n```\n[{\'keyword\': \'python\', \'score\': 402}, {\'keyword\': \'language\', \'score\': 68}, {\'keyword\': \'software\', \'score\': 47}]\n```\n\n## Sentiment Analysis\n\nWe can also analyze the sentiment of an article with the **analyze_sentiment function**. This function returns a Sentiment object with sentiment and polarity attributes.\n\n```\nsentiment = tldr.analyze_sentiment(\'https://en.wikipedia.org/wiki/Python_(programming_language)\')\nprint(sentiment.json)\n```\n\nThe code above gives a dictionary with the sentiment and polarity of the article.\n\n```\n{\'sentiment\': \'positive\', \'polarity\': 0.10235096701177092}\n```\n',
    'author': 'Amol Mavuduru',
    'author_email': 'amolmavuduru@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AmolMavuduru/tldr-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
