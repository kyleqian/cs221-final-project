import songwriter
import search
import random
import os
import json
import sys
from datetime import datetime

class TaylorTester():
	def __init__(self, ucs, genre, baseline_flag=False, true_random=True):
		self.BASELINE_FLAG = baseline_flag
		self.GENRE = genre
		self.NUM_LINES_TESTED = 100
		self.ucs = ucs
		self.taylor_lyrics = [] # continuous list of lists of words, so list of lines of songs
		self.corpus = set()
		self.random = random
		if not true_random:
			self.random.seed(42)
		self.__read_lyrics()

	def evaluate(self):
		num_correct = 0
		num_examples = 0
		results = []

		# (unfilled lyric matrix, list of (line number, word index))
		unfilled_lyrics,fill_list = self.__generate_unfilled_lyrics()

		# filled lyric matrix
		filled_lyrics = self.__fill_lyrics(unfilled_lyrics, fill_list)

		for line_number,word_index in fill_list:
			line = list(filled_lyrics[line_number])
			line[word_index] = '[%s]' % line[word_index]
			num_examples += 1

			filled_line = ' '.join(line)
			print '\n', filled_line

			while True:
				response = raw_input('Does this word make sense in this spot? (y/n) >> ')
				if response == 'y':
					filled_line += '\ny\n\n'
					num_correct += 1
					break
				elif response == 'n':
					filled_line += '\nn\n\n'
					break
				else:
					continue
			results.append(filled_line)

		### logging
		score = (100.0 * num_correct / num_examples)
		header = 'baseline' if self.BASELINE_FLAG else 'ai'
		path = '%s/logs/%s-%s-%s.txt' % (os.path.dirname(os.path.realpath(__file__)), header, self.GENRE, str(datetime.now()))
		with open(path, 'w') as f:
			for x in results:
				f.write(x)
			f.write('\n')
			f.write('Good examples: %d\n' % num_correct)
			f.write('Total examples: %d\n' % num_examples)
			f.write('Score: %f%%' % score)

		print '\nFinished! Results have been logged.'
		print 'Good examples: %d' % num_correct
		print 'Total examples: %d' % num_examples
		print 'Score: %f%%' % score

	def __read_lyrics(self):
		with open('stripped_taylor.json', 'r') as f:
			lyrics = json.loads(f.read())
			for song in lyrics:
				for line in lyrics[song]:
					list_of_words = line.split()
					self.taylor_lyrics.append(list_of_words)
					if self.BASELINE_FLAG:
						for word in list_of_words:
							self.corpus.add(word)

	# returns (selected lines, list of (line number, word index))
	def __generate_unfilled_lyrics(self):
		fill_list = []
		selected_lines = random.sample(self.taylor_lyrics, self.NUM_LINES_TESTED)

		### remove words
		for i,line in enumerate(selected_lines):
			if len(line) > 2:
				index_to_remove = random.randint(1, len(line) - 1)
				line[index_to_remove] = '_'
				fill_list.append((i, index_to_remove))

		return (selected_lines, fill_list)

	# returns filled lyric matrix
	def __fill_lyrics(self, unfilled_lyrics, fill_list):
		if not self.BASELINE_FLAG:
			sw = songwriter.SongWriter(self.GENRE, unfilled_lyrics)
			self.ucs.solve(sw)
			if ucs.finalState.lyrics is not None:
				return ucs.finalState.lyrics
			else:
				raise Exception('No solution found')

		else:
			filled_lyrics = list(unfilled_lyrics)
			for line_number,word_index in fill_list:
				random_word = self.random.sample(self.corpus, 1)
				filled_lyrics[line_number][word_index] = list(random_word)[0]
			return filled_lyrics

	def print_lyrics(self, title):
		for line in self.taylor_lyrics:
			print ' '.join(line)

if __name__ == '__main__':
	baseline_flag = True if '-b' in sys.argv else False
	while True:
		genre = raw_input('What genre? (country, hiphoprap, or pop) >> ')
		if genre in ['country', 'hiphoprap', 'pop']:
			break		

	ucs = search.UniformCostSearch(0)
	t = TaylorTester(ucs, genre, baseline_flag)
	t.evaluate()
