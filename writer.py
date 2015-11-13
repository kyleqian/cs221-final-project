import util
import random
from copy import deepcopy

class SongState():
	def __init__(self, genre):
		self.genre = genre
		self.max_lines = util.generateNumSongLines(self.genre)
		# self.max_words_per_line = util.generateMaxWordsInLine(self.genre) # TODO
		self.lyrics = [['_']*util.generateMaxWordsInLine(self.genre) for _ in xrange(self.max_lines)]
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
		
		return state

	def __get_next_blank(self, state):
		for line_number,line in enumerate(state.lyrics):
			if self.blank_marker in line:
				return (line_number,line.index(self.blank_marker))
		return None
				
	def __get_possible_words(self, state, line_number, line_position):
		words = []
		prev_word = state.lyrics[line_number][line_position - 1] #WHAT IF FIRST WORD

		### generate next words
		words.append('hi')
		return words

	def __calculate_cost(self, state, next_word, line_number, line_position):
		### calculate cost of adding next_word in state at given line number and position
		return 1

	def start_state(self):
		state = SongState(self.genre)
		return self.__generate_seeds(state)

	def is_goal(self, state):
		return self.__get_next_blank(state) == None

	def succ_and_cost(self, state):
		successors = []
		line_number,line_position = self.__get_next_blank(state)

		possible_words = self.__get_possible_words(state, line_number, line_position)

		for w in possible_words:
			next_state = deepcopy(state)
			next_state.lyrics[line_number][line_position] = w
			cost = self.__calculate_cost(state, w, line_number, line_position)
			successors.append((w, next_state, cost))

		return successors


w = Writer('country')
ss = w.start_state()
suc = w.succ_and_cost(ss)
print suc