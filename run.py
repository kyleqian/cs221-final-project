import util

ignoredWords = util.parseIgnoredWords("ignore.txt")
genreDict = util.readExamples("country.txt", "country", ignoredWords)