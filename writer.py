import util
import random

class SongState():
	def __init__(self, genre):
		self.genre = genre
		self.max_lines = util.generateNumSongLines(self.genre)
		# self.max_words_per_line = util.generateMaxWordsInLine(self.genre) # TODO
		self.lyrics = [['_']*util.generateMaxWordsInLine(self.genre) for _ in xrange(self.max_lines)]
		self.current_line = None # pointer to current line in self.lyrics
		self.current_line_number = 0
		# numSyllablesInLine = util.syllable_count(word)
		# rhymingWords = util.findRhymes(words)	

class Writer():
	def __init__(self, genre):
		self.genre = genre
		self.genre_db = util.readExamples(genre)
		self.blank_marker = '_'

	# weighted random word for each start of line
	def __generate_seeds(self, state):
		for line in state.lyrics:
			seed_word = util.chooseRandomGram(self.genre_db, self.genre)
			line[0] = seed_word
		
		state.current_line = state.lyrics[0]
		return state

	def __get_next_blank(self, state):
		for line_number,line in enumerate(state.lyrics):
			if self.blank_marker in line:
				return line_number,line.index(self.blank_marker)
				

	def start_state(self):
		state = SongState(self.genre)
		return self.__generate_seeds(state)

	def is_goal(self, state):
		return len(state.lyrics[len(state.lyrics - 1)]) == state.max_words_per_line

	def succ_and_cost(self, state):
		line_number,line_position = self.__get_next_blank(state)


w = Writer('country')
ss = w.start_state()