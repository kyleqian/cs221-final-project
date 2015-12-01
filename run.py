import util
import search
import songwriter
import tagger

ignoredWords = util.parseIgnoredWords("ignore.txt")
genre = "country"
genreDict = util.readExamples(genre, ignoredWords)

# ucs = search.UniformCostSearch(0)
# w = writer.Writer(genre)
# ucs.solve(w)
# print ucs.finalState.lyrics

#lyrics = util.createSong(genre, 0.01)
ucs = search.UniformCostSearch(0)
w = songwriter.SongWriter(genre)
ucs.solve(w)
print ucs.finalState.lyrics