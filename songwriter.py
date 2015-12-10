import util
import random
from copy import deepcopy
import tagger




class SongState():
	def setPartOfSpeechGrid(self, grid):
		self.partOfSpeechGrid = grid
		self.max_lines = len(grid)
		lyrics = []
		for line in grid:
			l = len(line)
			arr = ["_"]*l
			lyrics.append(arr)
		self.lyrics = lyrics



	def __init__(self, genre, startLyrics=None):
		self.genre = genre
		#self.max_lines = util.generateNumSongLines(self.genre)
		self.max_lines = 20
		# self.max_words_per_line = util.generateMaxWordsInLine(self.genre) # TODO
		#self.lyrics = [['_']*util.generateMaxWordsInLine(self.genre) for _ in xrange(self.max_lines)]
		blankValues = [6,7,8,9]
		lyrics = []
		for _ in xrange(self.max_lines):
			#num = random.choice(blankValues)
			arr = ['_']*8
			lyrics.append(arr)

		self.lyrics = lyrics
		self.partOfSpeechGrid = []
		# numSyllablesInLine = util.syllable_count(word)
		# rhymingWords = util.findRhymes(words)	

class SongWriter():
	def __init__(self, genre, startLyrics=None):
		self.genre = genre
		self.genre_db = util.readExamples(genre)
		self.blank_marker = '_'
		self.startLyrics = startLyrics
		self.ceiling = 1000000
		self.bigramCeiling = 100000
		self.trigramCeiling = 10000
		self.fourgramCeiling = 1000
		self.tagger = tagger.Tagger()		
		self.cache = {}
		self.rhymeCache = {}
		self.syllableCache = {}
		self.endingCache = {}
		self.numBigrams = 0
		self.numTrigrams = 0
		self.numFourgrams = 0
		self.sentenceEndingFloor = 50


	def getCachedEndingCheck(self,s):
		arr = s.split(" ")
		if len(arr) > 4:
			arr = arr[-4:]
		s = " ".join(arr)
		if s in self.endingCache:
			return self.endingCache[s]
		return None

	def setCachedEndingCheck(self,s, v):
		arr = s.split(" ")
		if len(arr) > 4:
			arr = arr[-4:]
		s = " ".join(arr)

		self.endingCache[s] = v

	def getCachedDeduction(self,s):
		arr = s.split(" ")
		if len(arr) > 4:
			arr = arr[-4:]
		s = " ".join(arr)

		if s in self.cache:
			return self.cache[s]
		return None

	def setCachedDeduction(self,s, d):
		arr = s.split(" ")
		if len(arr) > 4:
			arr = arr[-4:]
		s = " ".join(arr)

		self.cache[s] = d

	def getCachedRhymeDeduction(self, s1, s2):
		if (s1,s2) in self.rhymeCache:
			return self.rhymeCache[(s1,s2)]
		if (s2,s1) in self.rhymeCache:
			return self.rhmyeCache[(s2,s1)]
		return None

	def setCachedRhymeDeduction(self, s1, s2,d):
		self.rhymeCache[(s1,s2)] = d
		self.rhymeCache[(s2,s1)] = d

	def __generate_seeds(self, state):
		wordsToPOSMap = self.genre_db[self.genre]["wordsToPosMap"]
		posToWordsMap = self.genre_db[self.genre]["posToWordsMap"]
		sentenceBeginnings = self.genre_db[self.genre]["sentenceBeginnings"]
		for i in range(len(state.lyrics)):
			line = state.lyrics[i]
			pos = state.partOfSpeechGrid[i][0]
			possibleWords = posToWordsMap[pos]

			intersection = self.intersection(sentenceBeginnings, possibleWords)
			if len(intersection) == 0:
				print "WARNING! NO WORDS FOUND IN THE INTERSECTION OF TWO ARRAYS IN START STATE"
				exit()
			
			seed_word = random.choice(intersection)
			#seed_word = util.chooseRandomGram(self.genre_db, self.genre)
			line[0] = seed_word
		
		return state

	def start_state(self):
		numLines = 10
		if self.startLyrics is None:
			grid = self.generateRandomPOSGrid(numLines)
			state = SongState(self.genre)
			state.setPartOfSpeechGrid(grid)
			return self.__generate_seeds(state)
		else:
			state = SongState(self.genre)
			state.lyrics = self.startLyrics
			#print state.lyrics
			return state

	def __get_next_blanks(self, state):
		linePosArr = []
		for line_number,line in enumerate(state.lyrics):
			if self.blank_marker in line: # (1, 5) where 5 is the index of the blank marker
				linePosArr.append(line.index(self.blank_marker))
			else: #(1, None) where None means that there are no words left to fill
				linePosArr.append(None)
		return linePosArr

	def __get_num_blanks_remaining(self,state):
		total = 0
		for i,line in enumerate(state.lyrics):
			for word in line:
				if word == self.blank_marker:
					total += 1
		return total

	
	"""
	COST CALCULATION
	"""

	def getBigramCost(self, prev_word, next_word):
		bigram = prev_word + " " + next_word
		bigramFreq = self.genre_db[self.genre]["bigrams"]
		if bigramFreq.get(bigram) is None:
			return self.ceiling
		else:
			bigramCost = bigramFreq[bigram]
			return self.bigramCeiling - bigramCost

	def getTrigramCost(self, word1, word2, word3):
		trigram = "%s %s %s" % (word1, word2, word3)
		trigramFreq = self.genre_db[self.genre]["trigrams"]
		if trigramFreq.get(trigram) is None:
			return self.ceiling
		else:
			trigramCost = trigramFreq[trigram]
			return self.trigramCeiling - trigramCost

	def getFourGramCost(self, w1, w2, w3, w4):
		fourGram = "%s %s %s %s" % (w1, w2, w3, w4)
		fourGramFreq = self.genre_db[self.genre]["fourgrams"]
		if fourGramFreq.get(fourGram) is None:
			return self.ceiling
		else:
			fourGramCost = fourGramFreq[fourGram]
			return self.fourgramCeiling - fourGramCost

	#cuts cost in half
	def getValidSentenceCostDeduction(self,s,cost):
		endings = self.genre_db[self.genre]["sentenceEnds"]
		if s in endings:
			return int(cost * 0.5)
		return 0
		# if self.tagger.sentenceEndingIsValid(s):
		# 	return int(cost * 0.5)
		# return 0

	def isValidSentenceEnding(self,s):
		endings = self.genre_db[self.genre]["sentenceEnds"]
		return s in endings

	def getRhymeDeduction(self, w1,w2,cost):
		rhymes1 = util.findRhymes(w1)
		rhymes2 = util.findRhymes(w2)
		if w2 in rhymes1 or w1 in rhymes2:
			return int(cost * 0.8)
		return 0

	def getSyllableCostDeduction(self, state, assignment,cost):
		sqdev = 0
		totalNumSyllables = 0
		for i in range(len(assignment)):
			p, next_word = assignment[i]
			totalNumSyllables += self.getNumSyllablesInLine(state.lyrics[i])
			if next_word is None:
				continue
			totalNumSyllables += self.getNumSyllablesInWord(next_word)

		averageSyllables = totalNumSyllables / len(assignment)
		for i in range(len(assignment)):
			p, next_word = assignment[i]
			lineCount = self.getNumSyllablesInLine(state.lyrics[i])

			if next_word is not None:
				lineCount += self.getNumSyllablesInWord(next_word)	
			sqdev += (abs(lineCount - averageSyllables))**2

		#print sqdev
		return cost * (cost / (cost + sqdev));




	# assignments contains tuples consisting of
	# (line_position, word_to_be_assigned)
	# note: i is the line number when iterating through the assignments
	#
	# return value: overall cost
	#
	# TODO: Decrease the costs based on things such as:
	# 	- syllables in sentence
	#   - valid part of speech assignment

	def getNumSyllablesInWord(self, w):
		ct = 0
		if w in self.syllableCache:
			ct = self.syllableCache[w]
		else:
			ct = util.syllable_count(w)
			self.syllableCache[w] = ct
		return ct

	def getNumSyllablesInLine(self, l):
		total = 0
		line = " ".join(l)
		if line in self.syllableCache:
			total = self.syllableCache[line]
		else:
			for w in l:
				total += self.getNumSyllablesInWord(w)
			self.syllableCache[line] = total
		return total

	def getNumPossiblePosMatches(self, state, line_number):
		nonBlankCount = 0
		line = state.lyrics[line_number]
		for word in line:
			if word != self.blank_marker:
				nonBlankCount += 1
		return nonBlankCount

	def getPartOfSpeechPoints(self, state, line_number):
		currGridLine = state.partOfSpeechGrid[line_number]
		line = state.lyrics[line_number]
		wordsToPosMap = self.genre_db[self.genre]["wordsToPosMap"]

		total = self.getNumPossiblePosMatches(state,line_number)
		ct = 0
		for p in range(len(line)):
			word = line[p]
			if word == self.blank_marker:
				break
			if word in wordsToPosMap:
				partsOfSpeech = wordsToPosMap[word]
				currPos = currGridLine[p]
				if currPos in partsOfSpeech:
					ct += 1
			else:
				print "word - %s - not in words " % word
			
		points = 20000 * ct / total
		return 20000 - points

	"""
	GRAM points:

	A value from 0 - 1000.

	Calculated by taking a fraction of the total number of 
	possible grams formed. In a perfect sentence. The total
	number of possible grams will be equal to the sum of

	numBigrams = len(sentence) - 1
	numTrigrams = len(sentence) - 2
	numFourgrams = len(sentence) - 3

	if a complete match is found, the score of that sentence will 
	be 0 (1000 - 1000 * fract) where fract is equal to

	numGramsFound / totalPossiblegrams

	For example, if len(sentence) == 8

	numBigrams = 7
	numTrigrams = 6
	numFourgrams = 5

	totalPossibleGrams: 18

	fract = n / 18, where n is the number of found grams

	"""

	def getNumPossibleGrams(self, line, n):
		nonBlankCount = 0
		for word in line:
			if word != self.blank_marker:
				nonBlankCount += 1
		numPossible = nonBlankCount - (n - 1)
		return numPossible if numPossible > 0 else 0

	def getNumGramMatches(self,line,n):
		start = 0
		if n == 2:
			start = 1
			matches = 0
			for i in range(start,len(line)):
				wordOneAway = line[i - 1]
				curr = line[i]
				bigram = "%s %s" % (wordOneAway, curr)
				bigramFreq = self.genre_db[self.genre]["bigrams"]
				if bigram in bigramFreq:
					matches += 1
			return matches
		elif n == 3:
			start = 2
			matches = 0
			for i in range(start,len(line)):
				wordTwoAway = line[i - 2]
				wordOneAway = line[i - 1]
				curr = line[i]
				trigram = "%s %s %s" % (wordTwoAway, wordOneAway, curr)
				trigramFreq = self.genre_db[self.genre]["trigrams"]
				if trigram in trigramFreq:
					matches += 1
			return matches
		elif n == 4:
			start = 3
			matches = 0
			for i in range(start,len(line)):
				wordThreeAway = line[i - 3]
				wordTwoAway = line[i - 2]
				wordOneAway = line[i - 1]
				curr = line[i]
				fourgram = "%s %s %s %s" % (wordThreeAway,wordTwoAway, wordOneAway, curr)
				fourgramFreq = self.genre_db[self.genre]["fourgrams"]
				if fourgram in fourgramFreq:
					matches += 1
			return matches
		return 0
		
			


	def getNumPossibleGramMatches(self, line):
		return self.getNumPossibleGrams(line, 2) + self.getNumPossibleGrams(line,3) + self.getNumPossibleGrams(line,4)

	def getGramPoints(self, state, line_number):
		line = state.lyrics[line_number]
		totalNumGrams = self.getNumPossibleGramMatches(line)
		
		ct = self.getNumGramMatches(line,2)
		ct += self.getNumGramMatches(line,3)
		ct += self.getNumGramMatches(line,4)

		points = 50000 * ct / totalNumGrams
		return 50000 - points

	def __calculate_cost(self, state, assignment):
		cost = 0
		for i in range(len(assignment)): # note i is the line number
			p, next_word = assignment[i]

			if p is None:
				continue
			
			state.lyrics[i][p] = next_word

			vals = [1,2,3,4,5,6,7,8,9,10]
			choice = random.choice(vals)
			points = 0
			if vals < 3:
				points = self.getGramPoints(state,i)
			else:
				points = self.getPartOfSpeechPoints(state,i)

			#gramPoints = self.getGramPoints(state,i)
			#posPoints = self.getPartOfSpeechPoints(state,i)
			state.lyrics[i][p] = self.blank_marker

			#cost += gramPoints
			cost += points

			# if p is None:
			# 	continue
			# costs = []
			# if p >= 1:
			# 	wordOneAway = state.lyrics[i][p - 1]
			# 	bigramCost = self.getBigramCost(wordOneAway, next_word)
			# 	costs.append(bigramCost)
			# 	if bigramCost < self.ceiling:
			# 		self.numBigrams += 1
			# if p >= 2:
			# 	wordTwoAway = state.lyrics[i][p - 2]
			# 	trigramCost = self.getTrigramCost(wordTwoAway, wordOneAway, next_word)
			# 	costs.append(trigramCost)
			# 	if trigramCost < self.ceiling:
			# 		self.numTrigrams += 1
			# if p >= 3:
			# 	wordThreeAway = state.lyrics[i][p - 3]
			# 	fourGramCost = self.getFourGramCost(wordThreeAway, wordTwoAway, wordOneAway, next_word)
			# 	costs.append(fourGramCost)
			# 	if fourGramCost < self.ceiling:
			# 		self.numFourgrams += 1
			# currcost = min(costs)


			# # cost based sentence ending
			# if p == len(state.lyrics[i]) - 1: # end of the line
			# 	arr = state.lyrics[i][:-1] + [next_word]
			# 	s = " ".join(arr)
			# 	deduction = self.getCachedDeduction(s)
			# 	if  deduction is None:
			# 		deduction = self.getValidSentenceCostDeduction(s, currcost)
			# 		self.setCachedDeduction(s,deduction)
			# 	# if deduction > 0:
			# 	# 	print "%s" % (s)
			# 	currcost -= deduction

			# if p == len(state.lyrics[i])  - 1:
			# 	arr = state.lyrics[i][:-1] + [next_word]
			# 	s = " ".join(arr)
			# 	v = self.getCachedEndingCheck(s)
			# 	if v is None:
			# 		v = self.isValidSentenceEnding(s)
			# 		self.setCachedEndingCheck(s, v)
			# 		if v:
			# 			print "VALID ENDING!!!"
			# 			currcost = self.sentenceEndingFloor
			# 	elif v:
			# 		print "VALID ENDING!!!"
			# 		currcost = self.sentenceEndingFloor	


			
			# if i % 2 == 1 and p == len(state.lyrics[i]) - 1:
			# 	w1 = assignment[i][1]
			# 	w2 = assignment[i - 1][1]
			# 	rhymeDeduction = self.getCachedRhymeDeduction(w1,w2)
			# 	if rhymeDeduction is None:
			# 		rhymeDeduction = self.getRhymeDeduction(w1, w2, currcost)
			# 		self.setCachedRhymeDeduction(w1, w2, rhymeDeduction)
			# 	if rhymeDeduction > 0:
			# 		print "%s|%s" % (w1,w2)
			# 	currcost -= rhymeDeduction

			# cost += currcost

		blanksRemaining = self.__get_num_blanks_remaining(state) - len(assignment) # an assignment has at least len(assignment) new words in it
		if blanksRemaining <= len(assignment): #only calculate the syllable count on the last iteration to pick the assignment with the least squared error
			cost -= self.getSyllableCostDeduction(state, assignment,cost)

			# if next_word in self.cache:
			# 	cost += self.cache[next_word]
			# else:
			# 	costs = []
			# 	if p >= 1:
			# 		wordOneAway = state.lyrics[i][p - 1]
			# 		bigramCost = self.getBigramCost(wordOneAway, next_word)
			# 		costs.append(bigramCost)
			# 	if p >= 2:
			# 		wordTwoAway = state.lyrics[i][p - 2]
			# 		trigramCost = self.getTrigramCost(wordTwoAway, wordOneAway, next_word)
			# 		costs.append(trigramCost)
			# 	if p >= 3:
			# 		wordThreeAway = state.lyrics[i][p - 3]
			# 		fourGramCost = self.getFourGramCost(wordThreeAway, wordTwoAway, wordOneAway, next_word)
			# 		costs.append(fourGramCost)
			# 	cost += min(costs)
			# 	self.cache[next_word] = cost
		# print cost
		return cost

	"""
	Assign a new word to each of the lines in the state. It will be based on a bigram, trigram, fourgram model
	An assignment = (lineNumber, [next_words])
	"""	

	def intersection(self,arr1, arr2):
		f = {}
		for obj in arr1:
			if obj not in f:
				f[obj] = obj
		arr1 = f.values()
		f = {}
		for obj in arr2:
			if obj not in f:
				f[obj] = obj
		arr2 = f.values()
		m = {}
		for obj in arr1:
			if obj not in m:
				m[obj] = 1
		result = []
		for obj in arr2:
			if obj in m:
				result.append(obj)
		return result


	def getPos(self,state, line_number, line_position):
		if line_number >= 0 and line_number < len(state.partOfSpeechGrid):
			line = state.lyrics[line_number]
			if line_position >= 0 and line_position < len(line):
				return state.partOfSpeechGrid[line_number][line_position]
		return None

	def __get_possible_words3(self, state, line_number, line_position):
		pos = self.getPos(state,line_number, line_position)
		if pos is not None:
			posToWordMap = self.genre_db[self.genre]["posToWordsMap"]
			posToWordList = posToWordMap[pos]
			wordList = self.__get_possible_words2(state, line_number, line_position)
			intersection = self.intersection(posToWordList, wordList)
			if len(intersection) > 0:
				return intersection
		return self.__get_possible_words2(state, line_number, line_position)



	def __get_possible_words2(self, state, line_number, line_position):
		wordThreeAway = None
		wordTwoAway = None
		wordOneAway = None

		line = state.lyrics[line_number]
		if line_position >= 1:
			wordOneAway = line[line_position - 1].lower()
		if line_position >= 2:
			wordTwoAway = line[line_position - 2].lower()
		if line_position >= 3:
			wordThreeAway = line[line_position - 3].lower()

		possibleWords = util.getPossibleWords(self.genre_db[self.genre],wordThreeAway, wordTwoAway, wordOneAway)
		if len(possibleWords) == 0:
			gram  = util.chooseRandomGram(self.genre_db, self.genre)
			return [gram]
		else:
			return possibleWords

	def __get_possible_words(self, state, line_number, line_position):
		prev_word = state.lyrics[line_number][line_position - 1].lower() #WHAT IF FIRST WORD
		gram_dict = util.getGramDict(self.genre_db[self.genre])
		if gram_dict.get(prev_word) is None:
			gram = util.chooseRandomGram(self.genre_db, self.genre)
			return [gram]
		possibleWords = gram_dict[prev_word]
		words = [word for word in possibleWords]
		return words

	def __get_possible_assignments(self, state):
		assignments = []
		blanks = self.__get_next_blanks(state)
		for lineNum in range(len(state.lyrics)):
			linePos = blanks[lineNum]
			if linePos is None:
				linePos = 0
				possibleWords = []
			else:
				possibleWords = self.__get_possible_words3(state, lineNum, linePos)
			assignments.append((linePos, possibleWords))
			

		combinations = self.getRandomCombinations(assignments)
		
		#combinations = self.getCombinations(assignments, [], 0)
		
		if len(combinations) > 5:
			combinations = combinations[0:5]
		#print combinations
		

		# final = []

		# for i in range(len(combinations)):
		# 	print combinations[i]
		# 	line_pos,combination = combinations[i]
		# 	arr = []
		# 	for j in range(len(combination)):
		# 		tup = (line_pos, combination[j])
		# 		arr.append(tup)
		# 	final.append(arr)
		#print final
		return combinations

	def getRandomCombinations(self, assignments):
		totalPossible = 1
		for i in range(len(assignments)):
			linePos, possibleWords = assignments[i]
			l = len(possibleWords)
			totalPossible *= l if l > 0 else 1
		numSamples = min(100,int(totalPossible * 0.4))

		#print "getting %i samples!" % numSamples
		combinations = []
		for i in range(numSamples):
			sample = self.getRandomCombination(assignments)
			#print sample
			if sample not in combinations:
				combinations.append(sample)
		return combinations


	def getRandomCombination(self,assignments):
		combination = []
		for assignment in assignments:
			linePos, possibleWords = assignment
			if len(possibleWords) > 0:
				word = random.choice(possibleWords)
				combination.append((linePos, word))
			else:
				combination.append((None,None))
		return combination


	# recursive function to get all possible combinations of assignments
	def getCombinations(self,assignments, result, elemIndex):
		if elemIndex == len(assignments):
			return [result]

		combinations = []
		line_pos,currAssignment = assignments[elemIndex]
		for k in range(len(currAssignment)):
			rCopy = result[:] # deep copy to prevent loose python scope from fucking shit up
			rCopy.append((line_pos,currAssignment[k]))
			currCombinations = self.getCombinations(assignments, rCopy, elemIndex + 1)
			combinations += currCombinations

		return combinations


	def is_goal(self, state):
		blanks = self.__get_next_blanks(state)
		for i in range(len(blanks)):
			if blanks[i] is not None:
				return False

		total = self.numBigrams + self.numTrigrams + self.numFourgrams
		if total > 0:
			bigramRatio = float(self.numBigrams)/ total
			trigramRatio = float(self.numTrigrams)/ total
			fourgramRatio = float(self.numFourgrams) / total
			print "2: %f | 3: %f | 4: %f" % (bigramRatio, trigramRatio, fourgramRatio)

		return True

	def succ_and_cost(self, state):
		successors = []

		assignments = self.__get_possible_assignments(state)
		for assignment in assignments:
			next_state = deepcopy(state)
			for lineNum in range(len(state.lyrics)): # assign next blank for each of the V a new word
				line_pos,next_word = assignment[lineNum]
				if line_pos >= len(next_state.lyrics[lineNum]) or line_pos is None:
					continue
				next_state.lyrics[lineNum][line_pos] = next_word
			cost = self.__calculate_cost(state, assignment)
			successors.append((assignment, next_state, cost))

		successors.sort(key=lambda tup: tup[2])  # sorts in place
		if len(successors) > 4:
			successors = successors[0:4]
		return successors

	def generateRandomPOSGrid(self, numLines):
		grid = []
		grammarTree = self.genre_db[self.genre]["grammarTreeMap"]
		for i in range(numLines):  #number of lines in song
			while(True):
				walk = util.randomWalk(grammarTree)
				if len(walk) <= 8 and len(walk) >= 6:
					grid.append(walk)
					break
		return grid



		