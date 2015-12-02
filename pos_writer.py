from nltk import pos_tag, word_tokenize
import nltk
import tagger
import util
import sys
from collections import Counter

def tagSentence(text):
	text = word_tokenize(text)
	return nltk.pos_tag(text)
def getStructure(text):
	tup = tagSentence(text)
	s = [t[1] for t in tup]
	return " ".join(s)

def createPartsOfSpeechFile(fileName, genre):
	fo = open(fileName, "w")
	genreDict = util.readExamples(genre)
	lines = genreDict[genre]["lines"]
	
	print len(lines)
	ct = 0
	structureMap = {}
	for line in lines:
		if ct == 5:
			break
		st = getStructure(line)
		print "%s | %s" % (st, line)
		splitArr = st.split(",")
		lineArr = line.split(",")
		for i in range(len(splitArr)):
			s = splitArr[i]
			l = lineArr[i]
			if structureMap.get(s) is None:
				arr = [l]
				structureMap[s] = (s, arr, 1)
			else:
				tup = structureMap[s]
				ct = tup[2] + 1
				arr = tup[1]
				arr += [l]
				structureMap[s] = (tup[0],arr, ct)
			
			ct += 1
		

	for k,tup in structureMap.iteritems():
		fo.write("%s|%s|%s" % (tup[0],tup[1], tup[2]))
		fo.write("\n")

	fo.close()
	
def main(argv):
	if argv is not None:
		genre = argv[0]
		fileName = "pos_" + genre + ".txt"		
		createPartsOfSpeechFile(fileName, genre)

if __name__ == "__main__":
   main(sys.argv[1:])