import util
import random
from copy import deepcopy

class SongState():
	def __init__(self, genre):
		self.genre = genre
		self.max_lines = util.generateNumSongLines(self.genre)
		self.max_lines = 2
		# self.max_words_per_line = util.generateMaxWordsInLine(self.genre) # TODO
        #self.lyrics = [['_']*util.generateMaxWordsInLine(self.genre) for _ in xrange(self.max_lines)]
		self.lyrics = [['_']*4 for _ in xrange(self.max_lines)]
		# numSyllablesInLine = util.syllable_count(word)
		# rhymingWords = util.findRhymes(words)	
class Writer():
	
	def __init__(self, genre, startLyrics=None):
		self.genre = genre
		self.genre_db = util.readExamples(genre)
		self.blank_marker = '_'
		self.startLyrics = startLyrics

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
		prev_word = state.lyrics[line_number][line_position - 1] #WHAT IF FIRST WORD
        	gram_dict = util.getGramDict(self.genre_db[self.genre]["lines"])
		#print gram_dict
		if gram_dict.get(prev_word) is None:
			gram = util.chooseRandomGram(self.genre_db, self.genre)
			return [gram]
        	possibleWords = gram_dict[prev_word]
        	words = [word for word in possibleWords]
        	return words

	def __calculate_cost(self, state, next_word, line_number, line_position):
                prev_word = state.lyrics[line_number][line_position - 1] #WHAT IF FIRST WORD
                bigram = prev_word + " " + next_word
		bigramFreq = self.genre_db[self.genre]["bigrams"]
		if bigramFreq.get(bigram) is None:
			return 10000000
                bigramCost = self.genre_db[self.genre]["bigrams"][bigram]
                return bigramCost

	def start_state(self):
		if self.startLyrics is None:
    			state = SongState(self.genre)
    			return self.__generate_seeds(state)
		else:
            		state = SongState(self.genre)
            		state.lyrics = self.startLyrics
			print state.lyrics
            		return state

	def is_goal(self, state):
		return self.__get_next_blank(state) == None

	def succ_and_cost(self, state):
		successors = []
		line_number,line_position = self.__get_next_blank(state)

		possible_words = self.__get_possible_words(state, line_number, line_position)
        
        	ct = 0
		for w in possible_words:
			if ct == 2: break
			#print state.lyrics
			next_state = deepcopy(state)
			next_state.lyrics[line_number][line_position] = w
			cost = self.__calculate_cost(state, w, line_number, line_position)
			successors.append((w, next_state, cost))
            		ct +=1

		return successors


w = Writer('country')
ss = w.start_state()
suc = w.succ_and_cost(ss)
