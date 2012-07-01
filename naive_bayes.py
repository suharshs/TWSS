"""
This file will contain the class and logic for the checking if a given sentence is a twss joke
Author : Suharsh Sivakumar
Date : June 30, 2012
"""

from operator import mul
import yaml
import string
import urllib
import re

class NaiveBayesClassifier:
	def __init__(self):
		stream = open('./data/positive_probs.yml')
		self.pos_probs = yaml.load(stream)
		stream.close()
		stream = open('./data/negative_probs.yml')
		self.neg_probs = yaml.load(stream)
		stream.close()
	def CheckSentence(self, sentence):
		pos_word_probs = []
		neg_word_probs = []
		words = self.Normalize(sentence)
		for word in words:
			if word in self.pos_probs and word in self.neg_probs:
				pos_word_probs.append(float(self.pos_probs[word]))
				neg_word_probs.append(float(self.neg_probs[word]))
		if pos_word_probs == []:
			return 0
		pos_prob = reduce(mul, pos_word_probs)
		if neg_word_probs == []:
			neg_prob = 0
		else:
			neg_prob = reduce(mul, neg_word_probs)
		return float(pos_prob)/(float(pos_prob)+float(neg_prob))
	def CheckSentences(self, sentence_list, threshold):
		valid_twss = []
		for sentence in sentence_list:
			prob = self.CheckSentence(sentence)
			if prob > threshold:
				valid_twss.append(sentence)
		return valid_twss
	def Normalize(self, sentence):
		words = []
		value = sentence.split()
		if len(value) > 0:
			words = words + value
		punc = set(string.punctuation)
		words = [''.join(ch for ch in word if ch not in punc) for word in words]
		words = [word.lower() for word in words if word.lower() not in "yet a about above after again against all am an and any are arent as at be because been before being below between both but by can cant cannot could couldnt did didnt do does doesnt dont down during each few for from further had hadnt has hasnt have havent having he hed hell hes her here heres hers herself him himself his how hows i id ill im ive if in into is isnt it its its itself lets me more most mustnt my myself no nor not of off on once only or other ought our ours  ourselves out over own same shant she shed shell shes should shouldnt so some such than that thats the their theirs them themselves then there theres these they theyd theyll theyre theyve this those through to too under until up very was wasnt we wed well were weve were werent what whats when whens where wheres which while who whos whom why whys with wont would wouldnt you youd youll youre youve your yours yourself yourselves".split()]
		return words
	def CheckFile(self, filename):
		stream = open(filename, 'r')
		#sentence_list = re.split('[.!?]',stream.read())
		line = stream.readline()
		sentence_list = []
		while line != '':
			sentence_list.append(line)
			line = stream.readline()
		stream.close()
		twss = self.CheckSentences(sentence_list, .95)
		return twss



