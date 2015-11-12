import os
import re
import json
from pprint import pprint
import util


class songState():
	

class songWriterBot():

	def startState(self,word):
		indexInLine = 0
		previousWords = []
		numPreviousLines = 0
		numSyllablesInLine = util.syllable_count(word)
		rhymingWords = util.findRhymes(word)
		return (indexInLine,previousWords,numPreviousLines,numSyllablesInLine,rhymingWords)


