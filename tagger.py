import string
def tagger(trainingSet):
	trainData = open(trainingSet,"r")
	trainDict = {}
	for line in trainData:
		sl = line.rstrip().split()
		if len(sl) == 2:
		    if sl[0] in trainDict:
			    if sl[1] not in trainDict[sl[0]]:
				    trainDict[sl[0]][sl[1]] = 1
			    else:
				    trainDict[sl[0]][sl[1]]+= 1
		    else:
			    trainDict[sl[0]] = {}
			    trainDict[sl[0]][sl[1]] = 1
                
                
	print trainDict


tagger("train")
