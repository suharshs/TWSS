"""
This file has the script that gets the positive and negative word data and stores them in yml files.
Author : Suharsh Sivakumar
Date : June 30, 2012
"""

from scrapers.scraper import *

twssscraper = TwssScraper()
fmlscraper = FmlScraper()
tflnscraper = TflnScraper()
for i in range(1,100):
	twssscraper.Execute('http://www.twssstories.com/best?page=%s' %(4*i))
	twssscraper.Execute('http://www.twssstories.com/best?page=%s' %(4*i-1))
	twssscraper.Execute('http://www.twssstories.com/best?page=%s' %(4*i-2))
	twssscraper.Execute('http://www.twssstories.com/best?page=%s' %(4*i-3))
	fmlscraper.Execute("http://www.fmylife.com/?page=%s" %i)
	tflnscraper.Execute("http://www.textsfromlastnight.com/texts-from-last-night/page:%s/type:Best/span:AllTime" %i)
words = fmlscraper.Words() + tflnscraper.Words()
twssscraper.WriteCountedWords('./data/positive.yml')
twssscraper.WriteProbabilities('./data/positive_probs.yml')
word_count = {}
TOTAL = 0
for word in words:
	if word in word_count:
		word_count[word] = word_count[word] + 1
	else:
		word_count[word] = 1
	TOTAL = TOTAL + 1
word_count['TOTAL'] = TOTAL
#Now create the probabilities
word_probs = {}
for key in word_count:
	word_probs[key] = float(word_count[key])/float(word_count['TOTAL'])
stream = open('./data/negative.yml', 'w')
yaml.dump(word_count, stream)
stream.close()
stream = open('./data/negative_probs.yml', 'w')
yaml.dump(word_probs, stream)
stream.close()
