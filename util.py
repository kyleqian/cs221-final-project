import os
import pronouncing
#########################################################################
# helper functions

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
    
def readExamples(path, genre, ignoredWords):
    '''
    Reads a set of training examples.
    
    
    @param path: file path: 
    @param genre: the key of the dictionary with the 
    '''
    lines = []
    for line in open(path):
        lines.append(line)
    
    # unigrams
    frequencies = extractWordFeatures(lines, None)
    sigFreq = extractWordFeatures(lines, ignoredWords)
    
    # bigrams
    bigramFreq = extractNGramFeatures(lines, 2)
    
    #trigrams
    trigramFreq = extractNGramFeatures(lines, 3)
    
    #4-grams
    fourGramFreq = extractNGramFeatures(lines, 4)
    
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
        
    examples.sort(key = lambda x: x[1])
    sigExamples.sort(key = lambda x: x[1])
    bigrams.sort(key = lambda x:x[1])
    trigrams.sort(key = lambda x:x[1])
    fourGrams.sort(key = lambda x:x[1])
    
    #print examples
    #print sigExamples
    #print bigrams
    #print trigrams
    print fourGrams
    
    genreDict = {}
    infoDict = {}
    infoDict["sortedUnigramCounts"] = examples
    infoDict["sortedSignificantCounts"] = sigExamples
    infoDict["sortedBigramCounts"] = bigrams
    infoDict["sortedTrigramCounts"] = trigrams
    infoDict["sortedFourgramCounts"] = fourGrams
    genreDict[genre] = infoDict
    
    return genreDict
    
