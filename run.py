import util
import search
import songwriter
import tagger
from collections import Counter
import random

# genre = "country"
# genreDict = util.readExamples(genre, ignoredWords)

# ucs = search.UniformCostSearch(0)
# w = writer.Writer(genre)
# ucs.solve(w)
# print ucs.finalState.lyrics

#lyrics = util.createSong(genre, 0.01)

# w = songwriter.SongWriter(genre)
# ucs.solve(w)
# lyrics =  ucs.finalState.lyrics

fo = open("songs.txt", "w")
fo.seek(0)
fo.truncate()
fo.write("CS 221 Songwriter AI\n")
fo.write("By: Alex Wells, Rob Resma, Kyle Qian\n\n\n")
fo.close()

numSongs = 10
genres = ["country", "hiphoprap", "pop"]
ctDict = Counter()

for i in range(numSongs):
	genre = random.choice(genres)
	ctDict[genre] += 1
	fileName = "songs.txt"
	fo = open(fileName, "a")
	ucs = search.UniformCostSearch(0)
	w = songwriter.SongWriter(genre)
	ucs.solve(w)
	lyrics =  ucs.finalState.lyrics

	"""
	Putting the lyrics that are calculated in a
	readable format to be saved in a text file.
	"""

	ct = ctDict[genre]
	genre = genre.capitalize()
	fo.write("%s Song %s\n\n" % (genre,ct))

	newLines = []
	for line in lyrics:
		newLine = []
		for word in line:
			newLine.append(str(word))
		newLines.append(" ".join(newLine))

	for line in newLines:
		print line
		fo.write(line)
		fo.write("\n")

	fo.write("\n\n\n\n")
	fo.close()













