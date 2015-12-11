from collections import defaultdict
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
		self.GENRE = 'hiphoprap'
		self.NUM_SAMPLES = 3
		self.PERCENT_OF_LINES_TESTED = 20
		self.ucs = ucs
		self.taylor_lyrics = defaultdict(list)
		self.corpus = set()
		self.__read_lyrics()
		self.random = random
		if not true_random:
			self.random.seed(42)

	def evaluate(self):
		num_correct = 0
		num_examples = 0
		results = []

		# list of (unfilled lyric matrix, list of (line number, word index))
		unfilled_songs = self.__generate_unfilled_songs()

		# list of (lyric matrix, list of (line number, word index))
		filled_songs = self.__fill_songs(unfilled_songs)

		for filled_song,fill_choices in filled_songs:
			for l,i in fill_choices:
				line = list(filled_song[l])
				line[i] = '[%s]' % line[i]
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
		header = 'baseline-' if self.BASELINE_FLAG else 'ai-'
		path = '%s/logs/%s%s.txt' % (os.path.dirname(os.path.realpath(__file__)), header, str(datetime.now()))
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
					self.taylor_lyrics[song].append(list_of_words)
					if self.BASELINE_FLAG:
						for word in list_of_words:
							self.corpus.add(word)

	def __generate_unfilled_songs(self):
		results = []
		titles = random.sample(self.taylor_lyrics.keys(), self.NUM_SAMPLES)
		for t in titles:
			lyrics_matrix = list(self.taylor_lyrics[t])

			### remove words
			tuples_of_lines_and_indices = []
			for i,line in enumerate(lyrics_matrix):
				if random.randint(1, 100) <= self.PERCENT_OF_LINES_TESTED:
					if len(line) > 2:
						index_to_remove = random.randint(1, len(line) - 1)
						line[index_to_remove] = '_'
						tuples_of_lines_and_indices.append((i, index_to_remove))

			results.append((lyrics_matrix, tuples_of_lines_and_indices))
		return results

	# lyrics is a list of lists containing individual words
	def __fill_songs(self, unfilled_songs):
		results = []

		if not self.BASELINE_FLAG:
			for unfilled_song,fill_list in unfilled_songs:
				sw = songwriter.SongWriter(self.GENRE, unfilled_song)
				self.ucs.solve(sw)
				if ucs.finalState.lyrics is not None:
					filled_song = ucs.finalState.lyrics
				else:
					print "No solution"
				results.append((filled_song, fill_list))

		else:
			for unfilled_song,fill_list in unfilled_songs:
				new_song = list(unfilled_song)
				for line_number,word_index in fill_list:
					random_word = self.random.sample(self.corpus, 1)
					new_song[line_number][word_index] = list(random_word)[0]
				results.append((new_song, fill_list))

		return results

	def print_lyrics(self, title):
		for line in self.taylor_lyrics[title]:
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
	# t.print_lyrics('You Belong With Me')