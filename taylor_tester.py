from collections import defaultdict
import songwriter
import search
import random

## TODO: SOME SONGS HAVE INVALID CHARACTERS
## TODO: RANDOM PRINT STATEMENTS
class TaylorTester():
	def __init__(self, genre, ucs):
		self.NUM_SAMPLES = 1
		self.genre = genre
		self.ucs = ucs
		self.taylor_lyrics = defaultdict(list)
		self.__read_lyrics()

	def evaluate(self):
		num_correct = 0
		num_examples = 0

		# list of (unfilled lyric matrix, list of (line number, word index))
		unfilled_songs = self.__generate_unfilled_songs()

		# list of (lyric matrix, list of (line number, word index))
		filled_songs = self.__fill_songs(unfilled_songs)

		for filled_song, fill_choices in filled_songs:
			for l,i in fill_choices:
				print '\n\n\n'
				line = list(filled_song[l])
				line[i] = '[%s]' % line[i]
				num_examples += 1
				print ' '.join(line)

				while True:		
					response = raw_input('Does this word make sense in this spot? (y/n) >> ')
					if response == 'y':
						num_correct += 1
						break
					elif response == 'n':
						break
					else:
						continue

		print '\nFinished!'
		print 'Good examples: %d' % num_correct
		print 'Total examples: %d' % num_examples
		print 'Score: %f%%' % (100.0 * num_correct / num_examples)

	def __read_lyrics(self):
		curr_song = ""
		for l in open('taylor-lyrics.txt', 'r'):
			line = l.strip().split()
			if len(line) > 0:
				if line[0] == '###':
					curr_song = ' '.join(line[1:])
				else:
					self.taylor_lyrics[curr_song].append(line)

	def __generate_unfilled_songs(self):
		results = []
		titles = random.sample(self.taylor_lyrics.keys(), self.NUM_SAMPLES)
		for t in titles:
			lyrics_matrix = list(self.taylor_lyrics[t])

			### remove words
			tuples_of_lines_and_indices = []
			for i,line in enumerate(lyrics_matrix):
				if len(line) > 1:
					line[1] = '_'
					tuples_of_lines_and_indices.append((i, 1))

			results.append((lyrics_matrix, tuples_of_lines_and_indices))
		return results

	def __fill_songs(self, unfilled_songs):
		results = []
		for unfilled_song,fill_list in unfilled_songs:
			sw = songwriter.SongWriter(self.genre, unfilled_song)
			self.ucs.solve(sw)
			filled_song = ucs.finalState.lyrics
			results.append((filled_song, fill_list))
		return results

	def print_lyrics(self, title):
		for line in self.taylor_lyrics[title]:
			print ' '.join(line)

genre = 'country'
ucs = search.UniformCostSearch(0)
t = TaylorTester(genre, ucs)
t.evaluate()
# t.print_lyrics('You Belong With Me')