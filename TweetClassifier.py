##########################################################################
## TweetClassification.py v0.3
##
## Implements tweet classification using machine learning and spark using HDFS
## This bounding box coordinates was used for NYC data
## Team Name: ANA
## Team Members : Anandh Varadarajan, Nithish Kolli, Abhiram Karri

from pyspark import SparkContext, SparkConf
import csv
import ast
import time
import sys
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import warnings
from pyspark.sql import SQLContext
from pyspark import sql
#import sqlContext_.implicits
warnings.filterwarnings("ignore")
#we initialize a dictionary of valid words using NLTK
dictionary = dict.fromkeys(words.words(), None)

#This is the feature space with 29 features that will be used to convert tweets to binary vector like OneHotEncoding
#Here we use Multilabel Binarizer for creating the vector
#derived from the word cloud for highly related accident related words
categories = ['accident', 'affecting', 'ambulance', 'blocked', 'blocking', 'blood', 'cause', 'caution', 'close',
              'closed', 'collision', 'delay','diversion', 'division', 'fatal','horrendous', 'incident', 'injured', 'involved',
              'junction', 'lane', 'minor', 'motorway', 'moving', 'police', 'road','rollover', 'serious', 'severe', 'mishap',
              'traffic', 'vehicle']

#Initializing the binarizer with given categories
mlb = MultiLabelBinarizer(classes=categories)

#defining the bounding box that will filter tweets based on UK. We can extend it to other places
def boundBox(x):
    #read as dictionary
    x[1] = ast.literal_eval(x[1])
    #filter tweets within a bounding box
    if((x[1]['coordinates'][0]>40.4774 and x[1]['coordinates'][0]<40.9176) and (x[1]['coordinates'][1]<-73.7004 and x[1]['coordinates'][1]>-74.2589)):
        return x

#defining the classify function that takes in the current tweet with the model created earlier to predict whether a tweet is
# accident related or not.
# 1 if accident, 0 if accident related or not
def classify(x,model):
    warnings.filterwarnings("ignore")
    encList = []
    #tokenize the tweet
    tokens = word_tokenize(x[0])
    #remove punctuations and special characters from the tweet
    punctuationLesswords = [word for word in tokens if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    # remove stop words from the tweet
    finalWords = [w.lower() for w in punctuationLesswords if not w in stop_words]
    ls = []
    #filter valid words
    for w in finalWords:
        try:
            word = dictionary[w]
            ls.append(w)
        except KeyError:
            continue
    #final list of words to be checked
    finalWords2 = ls
    encList.append(finalWords2)
    #binarize the tweet
    new_features = mlb.fit_transform(encList)
    #use the model to classify
    preds = model.predict(new_features)
    print("---------Current Tweet-----------")
    print(x[0])
    print("---------------------------------")
    print("\n")
    if(preds[0]==1):
        print("----------CLASSIFICATION RESULT -----------")
        print("This tweet is related to accident")
        print("-------------------------------------------")
        print()
        return [x[1]['coordinates'][0],x[1]['coordinates'][1]]
    else:
        print("----------CLASSIFICATION RESULT -----------")
        print("This tweet is NOT related to accident")
        print("-------------------------------------------")
        print("\n")

def analyzeAccidents(sc,w,model):
    headerData = w.first()
    geoInfoRDD = w.filter(lambda x: x != headerData).filter(lambda x: x!=None).filter(lambda x: x!=None).map(lambda x: [x[24],x[25]]).filter(lambda x: x[1]!='').map(lambda x:boundBox(x)).filter(lambda x: x!=None).map(lambda x:classify(x,model)).filter(lambda x: x!=None)
    finalCoordinatesForPlotting = geoInfoRDD.collect()
    for val in finalCoordinatesForPlotting:
        print(val)
    results = geoInfoRDD.toDF()
    #print(results)
    df = results.toPandas()
    df.to_csv("coordinates.csv")
    print("Input Data Read and Processed from official records for Plotting...")

if __name__ == "__main__":
    print("Starting to parse files")
    start = time.time()
    conff = SparkConf().setAppName("Final-Project").setMaster('local')
    sc = SparkContext(conf = conff)
    sqlContext = sql.SQLContext(sc)

    encList = []
    print("Training the model...")
    #train the model once with training set of 8k tweets with positive and negative values
    with open('d5.csv', 'r', encoding="utf-8") as file:
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

    new_features = mlb.fit_transform((encList))

    #Read the labels generated for training set to measure accuracy of the model
    #generateLabels.py was used to run to get the labels
    df = pd.read_csv('labelsFinal.csv')

    #b is an arbitrary column name
    labels = df['b'].to_numpy()
    print('Creating Training and Test Split...')
    train, test, train_labels, test_labels = train_test_split(new_features,
                                                              labels,
                                                              test_size=0.33,
                                                              random_state=40)
    gnb = GaussianNB()

    # Train our classifier
    print('Running the Naive Bayes to create the model...')
    model = gnb.fit(train, train_labels)
    print('Predicting for Test set')
    preds = gnb.predict(test)
    print('------------------------------------ Accuracy of Prediction on Test Set------------------------------------')
    print(str(float(accuracy_score(test_labels, preds))*100)+' %')
    nyc = sc.textFile(sys.argv[1]).mapPartitions(lambda line: csv.reader(line))
    analyzeAccidents(sc,nyc,gnb)