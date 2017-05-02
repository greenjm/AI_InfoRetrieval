import sys
import operator
import math
import nltk
from nltk.util import skipgrams
from os import listdir
from os.path import isfile, join

PROP_FILE = "properties"

def loadProps():
  d = {}
  with open(PROP_FILE) as f:
    for line in f:
       (key, val) = line.split()
       d[key] = int(val)
  return d

def countOccurrences(s, searchPath):
  occurrences = 0

  for f in listdir(searchPath):
    filePath = join(searchPath, f)
    if isfile(filePath):
      opened = open(filePath)
      contents = opened.read().lower()
      if s in contents:
        occurrences += 1
  return occurrences

def countGramOccurrences(gram, searchPath):
  occurrences = 0

  for f in listdir(searchPath):
    filePath = join(searchPath, f)
    if isfile(filePath):
      opened = open(filePath)
      contents = opened.read().lower()
      tokenized = contents.split()
      fileGrams = list(skipgrams(tokenized, 2, 2))
      if gram in fileGrams:
        occurrences += 1
  return occurrences

def docProps(filePath, s):
  f = open(filePath)
  contents = f.read().lower()
  return (contents.count(s), len(contents))

def totalGramOccurrences(filePath, gram):
  f = open(filePath)
  contents = f.read().lower()
  tokenized = contents.split()
  fileGrams = list(skipgrams(tokenized, 2, 2))
  return fileGrams.count(gram)

def scoreFile(filePath, occurrences, gramOccurrences, props, k, b):
  scores = []
  keys = list(occurrences.keys())
  grams = list(gramOccurrences.keys())
  for key, val in occurrences.iteritems():
    numDocs = props["N"]
    relevantGrams = [gram for gram in grams if key in gram]
    for gram in relevantGrams:
      val += gramOccurrences[gram]
    if len(relevantGrams) > 0:
      numDocs *= (len(relevantGrams) + 1)
    IDF = math.log((numDocs - val + 0.5) / (val + 0.5))
    docOccurrences, docLength = docProps(filePath, key)
    for gram in relevantGrams:
      docOccurrences += totalGramOccurrences(filePath, gram)
    calc = float(docOccurrences * (k + 1)) / (docOccurrences + k * (1 - b + b * (float(docLength) / props["avg"])))
    scores.append(IDF * calc)
  return abs(sum(scores))


def main(argv):
  if len(argv) != 3:
    sys.exit(1)

  props = loadProps()
  k = float(argv[1])
  b = float(argv[2])
  searchPath = "Presidents/output"

  query = str(raw_input("Enter a query: "))
  tokenized = [s.lower() for s in query.split()]

  occurrences = {}
  gramOccurrences = {}

  for s in tokenized:
    occurrences[s] = countOccurrences(s, searchPath)

  # Skip grams
  for gram in list(skipgrams(tokenized, 2, 2)):
    gramOccurrences[gram] = countGramOccurrences(gram, searchPath)

  ranks = {}

  for f in listdir(searchPath):
    filePath = join(searchPath, f)
    if isfile(filePath):
      ranks[f] = scoreFile(filePath, occurrences, gramOccurrences, props, k, b)

  sortedRanks = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)

  i = 0
  for key, val in sortedRanks:
    if i >= 10:
      break
    print("File: " + key + "\t Score: " + str(val))
    i += 1


if __name__=="__main__":
  main(sys.argv)