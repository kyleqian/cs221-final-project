import pronouncing
import util
import random
import sys
import copy

def isNum(w):
	return w.isdigit()

def turn1Through10IntoString(w):
	v = int(w)
	if v == 0:
		return "zero"
	if v == 1:
		return "one"
	if v == 2:
		return "two"
	if v == 3:
		return "three"
	if v == 4:
		return "four"
	if v == 5:
		return "five"
	if v == 6: 
		return "six"
	if v == 7:
		return "seven"
	if v == 8:
		return "eight"
	if v == 9:
		return "nine"
	return None

def turnNumIntoString(w):
	original = copy.deepcopy(w)
	if isNum(w):
		# check for 1-10
		v = turn1Through10IntoString(w)
		if v is not None:
			return v
		v = int(w)
		if v * 1000 == 0:
			return "thousand"
		if v % 100 == 0:
			return "hundred"
		w = w[-2:]
		v = int(w)
		if v >= 20 and v < 100: 
			if v % 10 == 0:
				return "tee"
			w = w[-1:]
			v = turn1Through10IntoString(w)
			if v is not None:
				return v
			print original
			return original
		elif v > 12 and v < 20: 
			return "teen"
		elif v == 12:
			return "twelve"
		elif v == 11:
			return "eleven"
		elif v == 10:
			return "ten"
		return original
	else:
		return original

def writeRhymes():
	countryInfo = util.readExamples("country")["country"]
	hiphoprapInfo = util.readExamples("hiphoprap")["hiphoprap"]
	popInfo = util.readExamples("pop")["pop"]

	wordMap = {}

	lines = countryInfo["lines"]
	lines += hiphoprapInfo["lines"]
	lines += popInfo["lines"]

	for line in lines:
		line = line.split(" ")
		for word in line:
			word = word.lower()
			if word not in wordMap:
				wordMap[word] = word

	values = wordMap.values()

	fo = open("rhymes.txt", "w")

	ct = 0
	for word in values:
		if "," in word:
			splitArr = word.split(",")
			for splitWord in splitArr:
				print "%i. finding rhyme for: %s" % (ct,splitWord)
				fo.write("%s:" % splitWord.encode('utf8')) 
				splitWord = turnNumIntoString(splitWord)
				rhymes = util.findRhymes(splitWord)
				for i in range(len(rhymes)):
					text = "%s," % rhymes[i] if i != len(rhymes) - 1 else "%s" % rhymes[i]
					fo.write(text.encode('utf8'))
				fo.write("\n")
				ct += 1
		else:
			print "%i. finding rhyme for: %s" % (ct,word)
			fo.write("%s:" % word.encode('utf8')) 
			word = turnNumIntoString(word)
			rhymes = util.findRhymes(word)
			for i in range(len(rhymes)):
				text = "%s," % rhymes[i] if i != len(rhymes) - 1 else "%s" % rhymes[i]
				fo.write(text.encode('utf8'))
			fo.write("\n")
			ct += 1
	fo.close()

#writeRhymes()
util.extractRhymeMap()

