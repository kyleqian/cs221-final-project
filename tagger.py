from nltk import pos_tag, word_tokenize
import nltk
from collections import Counter



class Tagger(object):
	def __init__(self):
		pass
		#self.lines = lines
		#self.structureMap = self.getSentenceStructureDict(lines)
		#self.structures = list(self.structureMap)
	def tagSentence(self, text):
		text = word_tokenize(text)
		return nltk.pos_tag(text)

	def sentenceEndingIsValid(self, text):
		splitArr = text.split(" ")
		if len(splitArr) > 4:
			splitArr = splitArr[:-4]
			text = " ".join(splitArr)
		lastToken = self.tagSentence(text).pop()[1]
		invalidLastTokens = ["DT", "AT", "JJ","CC", "EX", "IN", "JJR","MD","PDT","RP","TO","UH","VB", "VBD","VBG","VBN","VBP","VBZ", "WDT", "WP", "WP$","WRB", "PRP$", ",","PRP"];
		if lastToken in invalidLastTokens:
			return False
		print lastToken
		return True

	# def getStructure(self, text):
	# 	tup = self.tagSentence(text)
	# 	s = [t[1] for t in tup]
	# 	return " ".join(s)
	# def getSentenceStructureDict(self,lines):
	# 	structMap = Counter()
	# 	ct = 0
	# 	for line in lines:
	# 		print line
	# 		structure = self.getStructure(line)
	# 		print structure
	# 		structMap[structure] += 1
	# 		if ct == 10:
	# 			break;
	# 		ct += 1

	# 	return structMap
	# def __isValidAssignment(current, word):
	# 	structure = self.getStrucure(current + " " + word)
	# 	for currStruct in structures:
	# 		if structure in currStruct:
	# 			return True
	# 	return False

#print tagSentence("My name is Rob, and I would enjoy coding very much.")