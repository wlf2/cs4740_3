#!/usr/bin/env python
import os, os.path
import nltk
import pairing
from nltk.corpus import senseval

path = os.path.relpath('nltk_data')
nltk.data.path[0]=path

items = senseval.fileids()

tests = pairing.parse_file("EnglishLS.test/EnglishLS.test")

senses = []
for item in items:
	train=[]
	for instance in senseval.instances(item):
		pos = instance.position
		context = instance.context
		instance_senses = instance.senses

		d={}
		d['prev_word']=context[pos-1]
		d['actual_word']=context[pos]
		d['next_word']=context[pos+1]
		for sense in instance_senses:
			pair = (d,sense)
			train.append(pair)

	test=[]
	lexitem = ".".join(item.split(".")[0:2])
	for instance in tests[lexitem]:
		context = instance['context']
		pos = instance['position']

		d={}
		d['prev_word']=context[pos-1]
		d['actual_word']=context[pos]
		d['next_word']=context[pos+1]
		test.append(d)
	classifier = nltk.NaiveBayesClassifier.train(train)
	senseList = classifier.batch_classify(test)
	senses.extend(senseList)
	result = zip(senseList, [x['id_num'] for x in tests[lexitem]])
	#print result
	#print classifier.show_most_informative_features()

#file writing stuff.  Will not work in the initial implementation.
#requires all of words to have a sense
f = open('answers.txt')
#out = open('responses.txt', 'w')
l = []
for line in f:
  l.append(line)
for x in range(len(senseList)):
  print(l[x].rstrip().rstrip('\n') + " " + senses[x])
f.close()
#out.close()
#print senseList
#print classifier.show_most_informative_features()
