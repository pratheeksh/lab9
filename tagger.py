import string
import re
import csv
import math
minProb = -100000000
emitDict = {}
posDict ={}
transDict = {}
def emissionProb(word, pos):
    ret = float("-inf")
    if word in emitDict :
        if pos in emitDict[word]:
	   pairCount = emitDict[word][pos]
	   totCount = posDict[pos]
	   ret = float(pairCount)/totCount
	   return math.log(ret,2)
        else:
	   return ret
    else:
        #print "word not found", word
        posDict["UK"]+=1
        emitDict[word]={}
        emitDict[word]["UK"]=1
        return minProb


def transProb(pos1, pos2):
    ret = float("-inf")
    if pos1 in transDict:

        if pos2 in transDict[pos1]:
	   sumValues = posDict[pos1]
	   countpos2 = transDict[pos1][pos2]
	   ret = float(countpos2)/sumValues
	   return math.log(ret,2)
        else:
	   if pos2 == "UK":
	       transDict[pos1][pos2]=1
	       ret=  float(1)/posDict[pos1]
	   return ret
    else: return minProb
def tagger(trainingSet,testSet):
    trainData = open(trainingSet,"r")
    testData = open(testSet,"r")
    res = []
    sent = []
    for line in testData:
        l = line.rstrip()
        if len(l) > 0:
	   sent.append(l)
        else:
	   res.append(' '.join(sent))
	   sent = []
        
    prev = 'S'
    posDict[prev] = 0
    for line in trainData:
        sl = line.rstrip().split()
        if len(sl) == 2:

	   if sl[0] in emitDict:
	       if sl[1] not in emitDict[sl[0]]:
		  emitDict[sl[0]][sl[1]] = 1
	       else:
		  emitDict[sl[0]][sl[1]]+= 1
	   else:
	       emitDict[sl[0]] = {}
	       emitDict[sl[0]][sl[1]] = 1
	   if sl[1] not in posDict:
	       posDict[sl[1]] = 1
	   else:
	       posDict[sl[1]]+= 1
	   if prev not in transDict:
	       transDict[prev]={}
	       transDict[prev][sl[1]]=1

	   else:
	       if sl[1] not in transDict[prev]:
		  transDict[prev][sl[1]]=1
	       else:
		  transDict[prev][sl[1]]+=1
	   prev = sl[1]

        else:
	   prev = 'S'
	   posDict[prev]+=1

    posDict["UK"] = 0
    output = []
    for sent in res:
        output.append(viterbi(sent))
    f = open("out",'w')
    writer = csv.writer(f, delimiter = '\t')

    for line in output:
        for o in line:
	   f.write("%s\t%s\n" %(o[0],o[1]))
        f.write("\n")

def viterbi(sent):
    sentence = sent.split(' ')
    trellis = []
    backtrack = []
    l = len(sentence)
    posList = posDict.keys()
    for i in xrange(l+1):
        viterbi_scores = dict(zip(posList,[float("-inf")]*len(posList)))
        viterbi_backtrack = dict(zip(posList,['xyz']*len(posList)))
        if i == 0:
	   viterbi_scores['S'] =  0
	   viterbi_backtrack['S'] = 's'
        trellis.append(viterbi_scores)
        backtrack.append(viterbi_backtrack)
    for i in xrange(1,l+1):
        cur = sentence[i-1]
        for to_pos in posList:
	  trellis[i][to_pos]= float("-inf")
	  for from_pos in  posList:
	      score = trellis[i-1][from_pos]+transProb(from_pos,to_pos)+emissionProb(cur,to_pos)
	      if  math.isinf(trellis[i][to_pos]) or  score > trellis[i][to_pos]:
		 max_score  = score
		 trellis[i][to_pos]=score
		 backtrack[i][to_pos]= from_pos
        
    best =  max(trellis[l], key=lambda i: trellis[l][i])
    out = []
    for i in xrange(l,0,-1):
        out.append((sentence[i-1],best))
        try:
	   best =  backtrack[i][best]
        except KeyError:
	   print backtrack
	   print "keyError",i, sentence[i-1],best
    out.reverse()
    return out


tagger("WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos","WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_24.words")
