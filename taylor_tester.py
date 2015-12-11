from collections import defaultdict
import songwriter
import search
import random
import os
import json
from datetime import datetime

class TaylorTester():
	def __init__(self, ucs):
		self.NUM_SAMPLES = 3
		self.PERCENT_OF_LINES_TESTED = 20
		self.TRUE_RANDOM = True
		self.GENRE = 'hiphoprap'
		self.ucs = ucs
		self.taylor_lyrics = defaultdict(list)
		self.__read_lyrics()

	def evaluate(self):
		num_correct = 0
		num_examples = 0
		results = []

		# list of (unfilled lyric matrix, list of (line number, word index))
		unfilled_songs = self.__generate_unfilled_songs()

		# list of (lyric matrix, list of (line number, word index))
		filled_songs = self.__fill_songs(unfilled_songs)

		for filled_song, fill_choices in filled_songs:
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
		with open(os.path.dirname(os.path.realpath(__file__)) + '/logs/' + str(datetime.now()) + '.txt', 'w') as f:
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
					self.taylor_lyrics[song].append(line.split())

		# curr_song = ''
		# for l in open('taylor-lyrics.txt', 'r'):
		# 	line = l.strip().split()
		# 	if len(line) > 0:
		# 		if line[0] == '###':
		# 			curr_song = ' '.join(line[1:])
		# 		else:
		# 			self.taylor_lyrics[curr_song].append(line)

	def __generate_unfilled_songs(self):
		if not self.TRUE_RANDOM: random.seed(42)

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

	def __fill_songs(self, unfilled_songs):
		results = []
		for unfilled_song,fill_list in unfilled_songs:
			sw = songwriter.SongWriter(self.GENRE, unfilled_song)
			self.ucs.solve(sw)
			if ucs.finalState.lyrics is not None:
				filled_song = ucs.finalState.lyrics
			else:
				print "No solution"
			results.append((filled_song, fill_list))
		return results

	def print_lyrics(self, title):
		for line in self.taylor_lyrics[title]:
			print ' '.join(line)

if __name__ == '__main__':
	ucs = search.UniformCostSearch(0)
	t = TaylorTester(ucs)
	t.evaluate()
	# t.print_lyrics('You Belong With Me')