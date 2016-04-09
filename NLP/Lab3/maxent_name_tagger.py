import string
import itertools
import nltk
from nltk.tag import UnigramTagger, BigramTagger, ClassifierBasedTagger
from nltk.classify import MaxentClassifier
from nltk.tag.sequential import ClassifierBasedPOSTagger
import pickle
def trainer(trainingSet,testSet):
    trainData = open(trainingSet,"r")
    testData = open(testSet,"r")
    res = []
    sent = []
    testRes =[]
    testlist = []
    prev_pos = '#'
    prev_chunk = ''
    pt = "#"
    for line in trainData:
        l = line.rstrip()
        if len(l) > 0:
	   word = l.split('\t')
	   word = word+[prev_pos,pt]
	   word[-2],word[-1]=word[-1],word[-2]
	   word[-3],word[-1]=word[-1],word[-3]
	   sent.append(tuple(word))
	   prev_pos = word[1]
	   prev_chunk = word[2]
	   pt = word[-1]
        else:
	   res.append(sent)
	   sent = []
    wordlist = []
    poslist = []
    testlist = []
    prev_pos = '#'
    prev_chunk = '#'
    for line in testData:

        l = line.rstrip()
        if len(l)>0:
	   sent = l.split('\t')
	   tup = dict(word=sent[0],pos=sent[1],chunk=sent[2],pp = prev_pos,pt="@@")
	   prev_pos = sent[1]
	   prev_chunk = sent[2]
	   testlist.append(tup)
   else:
	   
	   testRes.append(testlist)
	   wordlist = []
	   poslist = []
	   testlist = []
    test_sents=[]
    for sent in res:
        for w,t,c,ppos,prevtag,n in sent:
	   test_sents.append((dict(word=w,pos=t,chunk=c,pp=ppos,pt=prevtag),n))
    return test_sents[:10000], testRes

def parse():
    tagger_classes=([nltk.UnigramTagger, nltk.BigramTagger])
    trained_sents, tagged_sents =  trainer("CONLL_train.pos-chunk-name","CONLL_dev.pos-chunk")
    algorithm = 'GIS'
    classifier = nltk.classify.MaxentClassifier.train(trained_sents, algorithm, trace=0, max_iter=100)
    f = open('my_classifier2.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()
    f = open("final_myresponse_pickle_2",'w')
    for sent in tagged_sents:
        prev_tag = "#"
        for featureset in sent:
	   featureset['pt']=prev_tag
	   res = classifier.classify(featureset)
	   prev_tag=res
	   f.write("%s\t%s\n" %(featureset['word'],res))
        f.write("\n")
parse()
