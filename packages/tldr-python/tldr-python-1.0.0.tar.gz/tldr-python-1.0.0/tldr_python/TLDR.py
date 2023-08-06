import requests


class Summary(object):

	def __init__(self, summary_json):

		self.text = summary_json['summary']

class KeyWord(object):

	def __init__(self, word, score):

		self.word = word
		self.score = score


class KeyWordsList(object):

	def __init__(self, keywords_json):

		self.json = keywords_json
		self.keywords = [KeyWord(keyword['keyword'], keyword['score']) for keyword in self.json]


class Sentiment(object):

	def __init__(self, sentiment_json):

		self.sentiment = sentiment_json['sentiment']
		self.polarity = sentiment_json['polarity']
		self.json = sentiment_json


class TLDR(object):

	def __init__(self, rapidapi_key):

		self.rapidapi_key = rapidapi_key


	def summarize(self, text, max_sentences): 

		url = "https://tldr-text-analysis.p.rapidapi.com/summarize/"
		query_string = {"text": text, "max_sentences": str(max_sentences)}

		headers = {'x-rapidapi-key': self.rapidapi_key,
		           'x-rapidapi-host': "tldr-text-analysis.p.rapidapi.com"}

		response = requests.request("GET", url, headers=headers, params=query_string)

		if response.status_code == 200:
			return Summary(response.json())
		elif response.status_code == 404:
			raise ValueError("Could not extract text from URL. Please make sure the URL is valid.")
		else:
			raise Exception("Internal server error: the API could not process the request")


	def extract_keywords(self, text, n_keywords):

		url = "https://tldr-text-analysis.p.rapidapi.com/keywords/"
		query_string = {"text": text, "n_keywords": str(n_keywords)}

		headers = {'x-rapidapi-key': self.rapidapi_key,
		           'x-rapidapi-host': "tldr-text-analysis.p.rapidapi.com"}

		response = requests.request("GET", url, headers=headers, params=query_string)

		if response.status_code == 200:
			return KeyWordsList(response.json())
		elif response.status_code == 404:
			raise ValueError("Could not extract text from URL. Please make sure the URL is valid.")
		else:
			raise Exception("Internal server error: the API could not process the request")


	def analyze_sentiment(self, text):

		url = "https://tldr-text-analysis.p.rapidapi.com/sentiment_analysis/"
		query_string = {"text": text}

		headers = {'x-rapidapi-key': self.rapidapi_key,
		           'x-rapidapi-host': "tldr-text-analysis.p.rapidapi.com"}

		response = requests.request("GET", url, headers=headers, params=query_string)

		if response.status_code == 200:
			return Sentiment(response.json())
		elif response.status_code == 404:
			raise ValueError("Could not extract text from URL. Please make sure the URL is valid.")
		else:
			raise Exception("Internal server error: the API could not process the request")
		

