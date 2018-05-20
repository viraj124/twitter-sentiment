import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
        
short_pos = open("positive.txt","r").read()
short_neg = open("negative.txt","r").read()

documents = []
allowed_types=["J"]
all_words=[]
for r in short_pos.split('\n'):
    documents.append( (r, "pos") )
    words=word_tokenize(r)
    tags=nltk.pos_tag(words)
    for t in tags:
        if  t[1][0] in allowed_types:
            all_words.append(t[0].lower())

for r in short_neg.split('\n'):
    documents.append( (r, "neg") )
    words=word_tokenize(r)
    tags=nltk.pos_tag(words)
    for t in tags:
        if  t[1][0] in allowed_types:
            all_words.append(t[0].lower())


all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:5000]

def find_features(document):
    words=word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)

# positive data example:      
training_set = featuresets[:10000]
testing_set =  featuresets[10000:]

##
### negative data example:      
##training_set = featuresets[100:]
##testing_set =  featuresets[:100]

classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier_f1 = open("mnb.pickle", "rb")
MNB_classifier = pickle.load(classifier_f1)
classifier_f1.close()


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)

classifier_f2 = open("ber.pickle", "rb")
BernoulliNB_classifier = pickle.load(classifier_f2)
classifier_f2.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)

classifier_f3 = open("log.pickle", "rb")
LogisticRegression_classifier = pickle.load(classifier_f3)
classifier_f3.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)

classifier_f4 = open("lin.pickle", "rb")
LinearSVC_classifier = pickle.load(classifier_f4)
classifier_f4.close()

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)




voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)


def sentiment(text):
    feat=find_features(text)
    return (voted_classifier.classify(feat),voted_classifier.confidence(feat))
