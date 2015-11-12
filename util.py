import os
#import pronouncing
import re
#import nltk
import json
from pprint import pprint
import random

#########################################################################
# helper functions

def weightedRandomChoice(weightDict):
    weights = []
    elems = []
    for elem in weightDict:
        weights.append(weightDict[elem])
        elems.append(elem)
    total = sum(weights)
    key = random.uniform(0, total)
    runningTotal = 0.0
    chosenIndex = None
    for i in range(len(weights)):
        weight = weights[i]
        runningTotal += weight
        if runningTotal > key:
            chosenIndex = i
            return elems[chosenIndex]
    raise Exception('Should not reach here')

def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale
        
def findRhymes(word):
   return pronouncing.rhymes(word)

def syllable_count(word):
  """Uses an ad-hoc approach for counting syllables in a word"""
  # Count the vowels in the word
  # Subtract one vowel from every dipthong
  count = len(re.findall(r'([aeiouyAEIOUY]+)', word))
  # Subtract any silent vowels
  if len(word) > 2:
    if word[-1] == 'e' and  \
       not is_vowel(word[-2]) and \
       is_vowel(word[-3]):
      count = count - 1
  return count

###############################################################################
# parsers


def parseIgnoredWords(path):
    ignoredWords = []
    for line in open(path):
        ignoredWords.append(line.strip())
    return ignoredWords
    

def extractWordFeatures(lines, ignoredWords):
    frequencies = {}
    for line in lines:
        line = line.lower()
        split = line.split(" ")
        for word in split:
            if ignoredWords is None or (word not in ignoredWords):
                if frequencies.get(word) is None:
                    frequencies[word] = 0
                frequencies[word] += 1
    return frequencies

def extractNumLineFeatures(songs):
    frequencies = {}
    for song in songs:
        if len(song) in frequencies:
            frequencies[len(song)]+=1
        else:
            frequencies[len(song)]=1
    return frequencies

def generateNumSongLines(genre):
    lines = []
    with open('lyrics.json') as data_file:
        data = json.load(data_file) 
    numLineValues = extractNumLineFeatures(data[genre])
    numLineValuesArray = []
    for k,v in numLineValues.iteritems():
        for i in range(0,v):
            numLineValuesArray.append(k)
    print numLineValuesArray[random.randint(0,len(numLineValuesArray))]
    return numLineValuesArray[random.randint(0,len(numLineValuesArray))]

#generateNumSongLines('country')
            
def extractNGramFeatures(lines, n):
    if n > 6 or n < 1: return
    
    frequencies = {}
    for line in lines:
        line = line.lower()
        split = line.split()
        for i in range(len(split) - (n - 1)):
            gram = ""
            for j in range(n):
                word = split[i + j]
                gram += (word + " ")
            gram = gram[:-1]
            
            if frequencies.get(gram) is None:
                frequencies[gram] = 0
            frequencies[gram] += 1
    return frequencies
    
def extractSentenceLengthFeatures(lines):
    frequencies = {}
    for line in lines:
        length = len(line.split()) 
        if length not in frequencies:
            frequencies[length] = 1
        else:
            frequencies[length]+=1
    return frequencies

def extractSyllableFeatures(lines):
    frequencies = {}
    for line in lines:
        numSyllables = 0
        for word in line:
            numSyllables+=syllable_count(word)
        if numSyllables in frequencies:
            frequencies[numSyllables]+=1
        else:
            frequencies[numSyllables]=1
    #print frequencies
    return frequencies
def readExamples(genre, ignoredWords=None):
    '''
    Reads a set of training examples.
    
    
    @param path: file path: 
    @param genre: the key of the dictionary with the 
    '''
    lines = []
    with open('lyrics.json') as data_file:
        data = json.load(data_file)
    
    nestedArr = data[genre]    
    for song in nestedArr:
        for line in song:
            lines.append(line)
        
    #number of lines in each song
    songNumLineFeatures = extractNumLineFeatures(data[genre])
    
    #number of syllables in a line
    syllableFeatures = extractSyllableFeatures(lines)

    # unigrams
    frequencies = extractWordFeatures(lines, None)

    sigFreq = extractWordFeatures(lines, ignoredWords)
    
    # bigrams
    bigramFreq = extractNGramFeatures(lines, 2)
    
    #trigrams
    trigramFreq = extractNGramFeatures(lines, 3)
    
    #4-grams
    fourGramFreq = extractNGramFeatures(lines, 4)

    lengthFrequencies = extractSentenceLengthFeatures(lines)
    
    ###############################################
    ## methods
    examples = []
    for k,v in frequencies.iteritems():
        examples.append((k,v))
    
    sigExamples = []
    for k,v in sigFreq.iteritems():
        sigExamples.append((k,v))
        
    bigrams = []
    for k,v in bigramFreq.iteritems():
        bigrams.append((k,v))
        
    trigrams = []
    for k,v in trigramFreq.iteritems():
        trigrams.append((k,v))
    
    fourGrams = []
    for k,v in fourGramFreq.iteritems():
        fourGrams.append((k,v))

    numSongLines = []
    for k,v in songNumLineFeatures.iteritems():
        numSongLines.append((k,v))

    syllables = []
    for k,v in syllableFeatures.iteritems():
        syllables.append((k,v))

    examples.sort(key = lambda x: x[1])
    sigExamples.sort(key = lambda x: x[1])
    bigrams.sort(key = lambda x:x[1])
    trigrams.sort(key = lambda x:x[1])
    fourGrams.sort(key = lambda x:x[1])
    numSongLines.sort(key = lambda x:x[1])
    syllables.sort(key = lambda x:x[1])


    #print examples
    #print sigExamples
    #print bigrams
    #print trigrams
    #print fourGrams
    #print lengthFrequencies

    genreDict = {}
    infoDict = {}
    infoDict["unigrams"] = frequencies
    infoDict["syllableFeatures"] = syllables
    infoDict['songNumLineFeatures'] = numSongLines
    infoDict["sortedUnigramCounts"] = examples
    infoDict["sortedSignificantCounts"] = sigExamples
    infoDict["sortedBigramCounts"] = bigrams
    infoDict["sortedTrigramCounts"] = trigrams
    infoDict["sortedFourgramCounts"] = fourGrams
    genreDict[genre] = infoDict
    
    return genreDict
    
    
def chooseRandomGram(genre_db, genre):
    infoDict = genre_db[genre]
    unigrams = infoDict["unigrams"] 
    choice = weightedRandomChoice(unigrams)
    return choice
    
    
    
    
    
