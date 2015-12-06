from nltk import pos_tag, word_tokenize
import nltk
import tagger
import util
import json
import sys
from collections import Counter
from collections import defaultdict

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

def createPOSMaps():
	wordsToPOS = {}
	PosToWords = {}
	genres = ["country","hiphoprap","pop"]
	for g,genre in enumerate(genres):
		genreDict = util.readExamples(genre)
		sentences = genreDict[genre]["lines"]
		for i,sentence in enumerate(sentences):
			print "genre:{}, line:{}".format(genres[g],i)
			s = tagSentence(sentence)
			for tup in s:
				if tup[0] not in wordsToPOS:
					wordsToPOS[tup[0]]=[tup[1]]
				elif tup[1] not in wordsToPOS[tup[0]]: wordsToPOS[tup[0]].append(tup[1])
				if tup[1] not in PosToWords:
					PosToWords[tup[1]]=[tup[0]]
				elif tup[0] not in PosToWords[tup[1]]: PosToWords[tup[1]].append(tup[0])
	with open("wordsToPOS.json",'w+') as outfile1:
		outfile1.write(json.dumps(wordsToPOS,outfile1))
	with open("POSToWords.json",'w+') as outfile2:
		outfile2.write(json.dumps(PosToWords,outfile2))
	return

"""
This method will create a grammar tree.  My idea was to read in the lyrics.json file
and for each line of each song in the file, find out what the grammar structure of that 
line is.  Then using NLTK we can tag the line (therefore getting the parts of speech of each word
in the line).  Then we can add new nodes/append to the tree. 
"""		
def createGrammarTree(genre):
	def tree(): return defaultdict(tree)
	
	def add(t, path):
		for node in path:
			t = t[node]

	#genres = ["country", "hiphoprap", "pop"]
	genreDict = util.readExamples(genre)
	sentences = genreDict[genre]["lines"]
	grammarTree = tree()
	for i,sentence in enumerate(sentences):
		print i
		s = tagSentence(sentence)
		partsOfSpeech = [tup[1] for tup in s]
		add(grammarTree,partsOfSpeech)
	return grammarTree


"""
Given the current grammarTree and an array containing the parts of speech of 
a sentence (in order), will return the possible next parts of speech (empty array
if we haven't seen this sentence structure before)
"""
def traverseTree(grammarTree,partsOfSpeechArray):
	for item in partsOfSpeechArray:
		if item not in grammarTree: return []
		grammarTree = grammarTree[item]
	arr =  [item for item in grammarTree]
	return arr


def main(argv):
	#if len(sys.argv)!=3:
	#	print "USAGE: python pos_writer.py [genre] [outputfile]"
	#	exit(0)
	#outputfile = sys.argv[2]
	#genre = sys.argv[1]
	#t = createGrammarTree(genre)
	#with open(outputfile,'w+') as outfile:
	#	outfile.write(json.dumps(t,outfile))
	#createPOSMaps()
	with open("grammarTree_country.json") as datafile:
		data = json.loads(datafile.read())


	#writeTreeToFile(t,out)
	#out.close()
	#if argv is not None:
	#	genre = argv[0]
	#	fileName = "pos_" + genre + ".txt"		
	#	createPartsOfSpeechFile(fileName, genre)

if __name__ == "__main__":
   main(sys.argv[1:])
