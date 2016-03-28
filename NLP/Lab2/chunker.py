import string
import nltk
from nltk.tag import UnigramTagger, BigramTagger, ClassifierBasedTagger
from nltk.classify import MaxentClassifier
from nltk.tag.sequential import ClassifierBasedPOSTagger
def trainer(trainingSet,testSet):
    trainData = open(trainingSet,"r")
    testData = open(testSet,"r")
    res = []
    sent = []
    testRes =[]
    for line in trainData:
        l = line.rstrip()
        if len(l) > 0:
	   word = l.split('\t')
	   sent.append(tuple(word))
	   #sent.append(l)
        else:
	   res.append(sent)
	   sent = []
    #print res
    wordlist = []
    poslist = []
    for line in testData:

        l = line.rstrip()
        if len(l)>0:
	   word = l.split('\t')
	   wordlist.append(word[0])
	   poslist.append(word[1])
        else:
	   
	   testRes.append([wordlist,poslist])
	   wordlist = []
	   poslist = []
    test_sents = [] 
    test_sents = [[(t,c) for w,t,c in sent] for sent in res]
    #print test_sents 
    for sent in test_sents:
        if len(sent)==0:
	   test_sents.remove(sent)
    return test_sents, testRes

def parse():
    tagger_classes=([nltk.UnigramTagger, nltk.BigramTagger])
    trained_sents, tagged_sents =  trainer("WSJ_02-21.pos-chunk","WSJ_23.pos")
    #tagger = nltk.UnigramTagger(trained_sents)
    print len(trained_sents)
    tagger = ClassifierBasedPOSTagger(train=trained_sents[:10000], classifier_builder=lambda train_feats: 
    MaxentClassifier.train(train_feats, trace = 0,max_iter=10))
    f = open("WSJ_23.chunk",'w')
        #print sents
    for sents in tagged_sents:
        (words,tags)=sents[0],sents[1]
        chunks = tagger.tag(tags)
        #print words, chunks
        wtc = zip(words, chunks)


        for tup in wtc:
	   f.write("%s\t%s\n" %(tup[0],tup[1][1]))

        f.write("\n")

parse()
