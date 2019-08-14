##########################################################################
## generateLabels.py v0.2
##
## Generate labels for the training/validation set
## Here we extracted all the tweets for a specific time range and working with the subset
##
## Team Name: ANA
## Team Members : Anandh Varadarajan, Nithish Kolli, Abhiram Karri
##########################################################################

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
encList = []

dictionary = dict.fromkeys(words.words(),None)

categories = ['accident', 'affecting', 'ambulance', 'blocked', 'blocking', 'blood', 'cause', 'caution', 'close',
              'closed', 'collision', 'delay','diversion', 'division', 'fatal','horrendous', 'incident', 'injured', 'involved',
              'junction', 'lane', 'minor', 'motorway', 'moving', 'police', 'road','rollover', 'serious', 'severe', 'mishap',
              'traffic', 'vehicle']

encList = []
#we are using the tweet sample data to train the model
#We are basically processing the tweets and generating the binary vector after processing
with open('d5.csv','r',encoding="utf-8",errors='ignore') as file:
    for line in file:
        tokens = word_tokenize(line)
        punctuationLesswords = [word for word in tokens if word.isalpha()]

        stop_words = set(stopwords.words('english'))
        finalWords = [w.lower() for w in punctuationLesswords if not w in stop_words]
        ls = []
        for w in finalWords:
            try:
                x = dictionary[w]
                ls.append(w)
            except KeyError:
                continue
        finalWords2 = ls
        encList.append(finalWords2)


mlb = MultiLabelBinarizer(classes=categories)
#create the binary vector for all tweets
new_features = mlb.fit_transform((encList))

#Write all the labels generated for training/validation set
#Here we use the accident related ord cloud as dimensions/features and give unit score to them
#Based on analysis if the score is more than a given threshold, we pick the tweet, else not
with open('labelsFinal.csv','a+',encoding="utf-8") as file:
    file.write('b' + '\n')
    for i, vals in enumerate(new_features):
        if (np.sum(vals) > 2):
            file.write('1'+'\n')
        else:
            file.write('0'+'\n')
file.close()

