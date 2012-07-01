"""
This file contains the web scraper for acquiring the punch lines for twss jokes from twssstories.com
Author : Suharsh Sivakumar
Date : June 28, 2012
"""

import urllib
import re
#import nltk
import string
from operator import itemgetter
import yaml


class Scraper:
	regex = ''
	def __init__(self):
		self.words = []
		self.word_count = {}
		self.word_probs = {}
	def Execute(self, url):
		stream = urllib.urlopen(url)
		urlstring = stream.read()
		stream.close()
		sentence_list = re.findall(self.regex, urlstring)
		self.Normalize(sentence_list)
		#now calculate word_count
		word_count = {}
		TOTAL = 0
		for word in self.words:
			if word in word_count:
				word_count[word] = word_count[word] + 1
			else:
				word_count[word] = 1
			TOTAL = TOTAL + 1
		word_count['TOTAL'] = TOTAL
		self.word_count = word_count
		#Now create the probabilities
		word_probs = {}
		for key in self.word_count:
			word_probs[key] = float(word_count[key])/float(word_count['TOTAL'])
		self.word_probs = word_probs
	def Normalize(self, sentence_list):
		words = []
		for sentence_list_element in sentence_list:
			value = sentence_list_element.split()
			if len(value) > 0:
				words = words + value
		punc = set(string.punctuation)
		words = [''.join(ch for ch in word if ch not in punc) for word in words]
		words = [word.lower() for word in words if word.lower() not in "good want like much yet just put a about above after again against all am an and any are arent as at be because been before being below between both but by can cant cannot could couldnt did didnt do does doesnt dont down during each few for from further had hadnt has hasnt have havent having he hed hell hes her here heres hers herself him himself his how hows i id ill im ive if in into is isnt it its its itself lets me more most mustnt my myself no nor not of off on once only or other ought our ours  ourselves out over own same shant she shed shell shes should shouldnt so some such than that thats the their theirs them themselves then there theres these they theyd theyll theyre theyve this those through to too under until up very was wasnt we wed well were weve were werent what whats when whens where wheres which while who whos whom why whys with wont would wouldnt you youd youll youre youve your yours yourself yourselves".split()]
		self.words = self.words + words
	def Words(self):
		return self.words
	def CountedWords(self):
		return self.word_count
	def WriteCountedWords(self, filename):
		stream = open(filename, 'w')
		yaml.dump(self.word_count, stream)
		stream.close()
	def WriteProbabilities(self, filename):
		stream = open(filename, 'w')
		yaml.dump(self.word_probs, stream)
		stream.close()
	

class TwssScraper(Scraper):
	#Url that should be used: url = 'http://www.twssstories.com/best?page=%s'
	regex = "(?<=\")[^\"]+(?=\"[ ]*TWSS)"

class FmlScraper(Scraper):
	#Url that should be used: url = 'http://www.fmylife.com/?page=%s'
	regex = "(?<=\"fmllink\">)[^><]+(?=</a><a)"

class TflnScraper(Scraper):
	#Url that shoudl be used: url = 'http://www.textsfromlastnight.com/texts-from-last-night/page:%s/type:Best/span:AllTime'
	regex = "(?<=.html\">)[^><]+(?=</a></p>)"

"""
tflnscraper = TflnScraper()
for i in range(1,10):
	tflnscraper.Execute('http://www.textsfromlastnight.com/texts-from-last-night/page:%s/type:Best/span:AllTime' %i)
print tflnscraper.CountedWords()
"""



