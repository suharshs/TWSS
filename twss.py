"""
The command line tool for inputting files to the classifier.
Author : Suharsh Sivakumar
Date : July 1, 2012
"""

import sys
from naive_bayes import *

if len(sys.argv) == 1:
	print 'You must input a file that you want to test!'
	exit()
twss_list = []
for i in range(1, len(sys.argv)):
	 twss_list = twss_list + NaiveBayesClassifier().CheckFile(sys.argv[i])

for twss in twss_list:
	print twss