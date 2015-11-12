import util

class SongState():
	def __init__(self, genre):
		self.genre = genre
		self.max_lines = 10 # TODO
		self.max_words_per_line = 10 # TODO
		self.lyrics = [[] for _ in xrange(self.max_lines)]
		self.current_line = []
		self.current_line_number = 0
		# keep track of all other lines?
		# numSyllablesInLine = util.syllable_count(word)
		# rhymingWords = util.findRhymes(words)	

class Writer():
	def __init__(self, genre):
		self.genre = genre
		self.genre_db = util.readExamples(genre)

	# random word for each start of line
	def generate_seeds(self, state):
		for line in state.lyrics:
			line.append('hi')

	def start_state(self):
		state = SongState(self.genre)
		self.generate_seeds(state)
		return state

	def is_goal(self, state):
		return len(state.lyrics[len(state.lyrics - 1)]) == state.max_words_per_line

	def succ_and_cost(self, state):
		pass

w = Writer('country')
print w.start_state().lyrics