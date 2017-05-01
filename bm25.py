import sys
import operator
import math
from os import listdir
from os.path import isfile, join

PROP_FILE = "props.txt"

def loadProps():
  d = {}
  with open(PROP_FILE) as f:
    for line in f:
       (key, val) = line.split()
       d[key] = val
  return d

def countOccurrences(s, searchPath):
  occurences = 0

  for f in listdir(searchPath, f):
    filePath = join(searchPath, f)
    if isfile(filePath):
      opened = open(filePath)
      contents = opened.read().lower()
      if s in contents:
        occurences += 1
  return occurences

def docProps(filePath, s):
  f = open(filePath)
  contents = f.read().lower()
  return (contents.count(s), len(contents))

def scoreFile(filePath, occurrences, props, k, b):
  scores = []
  for key, val in occurrences:
    IDF = math.log((props["N"] - val + 0.5) / (val + 0.5))
    docOccurrences, docLength = docProps(filePath, key.lower())
    calc = float(docOccurrences * (k + 1)) / (docOccurrences + k * (1 - b + b * (float(docLength) / props["avg"])))
    scores.append(IDF * calc)
  return sum(scores)


def main(argv):
  if len(argv) != 3:
    sys.exit(1)

  props = loadProps()
  k = argv[1]
  b = argv[2]
  searchPath = "Presidents/"

  query = str(input("Enter a query: "))

  occurrences = {}

  for s in query.split():
    occurrences[s] = countOccurrences(s.lower(), searchPath)

  ranks = {}

  for f in listdir(searchPath):
    filePath = join(searchPath, f)
    if isfile(filePath):
      ranks[f] = scoreFile(filePath, occurrences, props, k, b)

  sortedRanks = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)

  for key, val in sortedRanks:
    print("File: " + key + "\t Score: " + str(val))


if __name__=="__main__":
  main(argv)