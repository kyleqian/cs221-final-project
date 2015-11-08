import os


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
        split = line.split(" ")
        for word in split:
            word = word.lower()
            if ignoredWords is None or (word not in ignoredWords):
                if frequencies.get(word) is None:
                    frequencies[word] = 0
                frequencies[word] += 1
    return frequencies

def extractBigramFeatures(lines):
    
    
def readExamples(path, genre, ignoredWords):
    '''
    Reads a set of training examples.
    
    
    @param path: file path: 
    @param genre: the key of the dictionary with the 
    '''
    genreDict = {}
    frequencies = {}
    sigFreq = {}
    
    lines = []
    for line in open(path):
        lines.append(line)
    
    # unigrams
    frequencies = extractWordFeatures(lines, None)
    sigFreq = extractWordFeatures(lines, ignoredWords)
    
    
    examples = []
    for k,v in frequencies.iteritems():
        examples.append((k,v))
    
    sigExamples = []
    for k,v in sigFreq.iteritems():
        sigExamples.append((k,v))
        
    examples.sort(key = lambda x: x[1])
    sigExamples.sort(key = lambda x: x[1])
    
    #print examples
    genreDict[genre] = examples
    return genreDict
    