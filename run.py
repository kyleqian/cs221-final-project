import util
import search
import writer

ignoredWords = util.parseIgnoredWords("ignore.txt")
genre = "hiphoprap"
genreDict = util.readExamples(genre, ignoredWords)
# ucs = search.UniformCostSearch(0)
# w = writer.Writer(genre)
# ucs.solve(w)
# print ucs.finalState.lyrics

lyrics = util.createSong(genre, 0.01)
ucs = search.UniformCostSearch(0)
w = writer.Writer(genre, lyrics)
ucs.solve(w)
print ucs.finalState.lyrics