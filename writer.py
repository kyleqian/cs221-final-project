import util

class SongState():
	def __init__(self, genre):
		self.genre = genre

	def generate_seed(self):
		pass

	

class Writer():
	def __init__(self, start_state, genre):
		self.genre_db = util.readExample(genre)
		self.start_state = start_state

	def startState(self, word):
		indexInLine = 0
		previousWords = []
		numPreviousLines = 0
		numSyllablesInLine = util.syllable_count(word)
		rhymingWords = util.findRhymes(word)
		return (indexInLine,previousWords,numPreviousLines,numSyllablesInLine,rhymingWords)


