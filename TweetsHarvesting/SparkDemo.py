#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:20:45 2017

@author: ellenk
"""

# Copied from Sentiment.py:
#

import sys
import time
import re
import nltk
from sklearn.externals import joblib
import json
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from kafka import KafkaProducer
# Processing Tweets

def preprocessTweets(tweet):
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)

    # Convert @username to __HANDLE
    tweet = re.sub('@[^\s]+', '__HANDLE', tweet)

    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    # trim
    tweet = tweet.strip('\'"')

    # Repeating words like happyyyyyyyy
    rpt_regex = re.compile(r"(.)\1{1,}", re.IGNORECASE)
    tweet = rpt_regex.sub(r"\1\1", tweet)

    # Emoticons
    emoticons = \
        [
            ('__positive__', [':-)', ':)', '(:', '(-:', \
                              ':-D', ':D', 'X-D', 'XD', 'xD', \
                              '<3', ':\*', ';-)', ';)', ';-D', ';D', '(;', '(-;', ]), \
            ('__negative__', [':-(', ':(', '(:', '(-:', ':,(', \
                              ':\'(', ':"(', ':((', ]), \
            ]

    def replace_parenth(arr):
        return [text.replace(')', '[)}\]]').replace('(', '[({\[]') for text in arr]

    def regex_join(arr):
        return '(' + '|'.join(arr) + ')'

    emoticons_regex = [(repl, re.compile(regex_join(replace_parenth(regx)))) \
                       for (repl, regx) in emoticons]

    for (repl, regx) in emoticons_regex:
        tweet = re.sub(regx, ' ' + repl + ' ', tweet)

        # Convert to lower case
    tweet = tweet.lower()

    return tweet


# Stemming of Tweets

def stem(tweet):
    stemmer = nltk.stem.PorterStemmer()
    tweet_stem = ''
    words = [word if (word[0:2] == '__') else word.lower() \
             for word in tweet.split() \
             if len(word) >= 3]
    words = [stemmer.stem(w) for w in words]
    tweet_stem = ' '.join(words)
    return tweet_stem


# Predict the sentiment

def predict(tweet, classifier):
    tweet_processed = stem(preprocessTweets(tweet))

    if (('__positive__') in (tweet_processed)):
        sentiment = 1
        return sentiment

    elif (('__negative__') in (tweet_processed)):
        sentiment = 0
        return sentiment
    else:

        X = [tweet_processed]
        sentiment = classifier.predict(X)
        return (sentiment[0])

#######################################################
# end of Sentiment.py
#########################################################




 
# Our filter function:
def filter_tweets(tweet):
    print("type(tweet): " + str(type(tweet)))
    json_tweet = json.loads(tweet)
    print("type(json_tweet): " + str(type(json_tweet)))

    if ( json_tweet["coordinates"] != None):
        print("filtering tweet")
        return True # filter() requires a Boolean value
    return False

# Enrich tweet & save to file
def process_to_file(rdd):
    print("processing rdd...")
    #rdd.filter( filter_tweets ).coalesce(1).saveAsTextFile("./tweets/%f" % time.time())
    enriched = rdd.map( lambda tweet: enrichTweet(tweet))
    enriched.coalesce(1).saveAsTextFile("./tweets/%f" % time.time())
    #enriched.foreach( lambda tweet: print("tweet: "+str(tweet)))


# Enrich tweet & send to Kafka
def process_to_kafka(rdd):
    print("processing rdd...")
    enriched = rdd.map( lambda tweet: enrichTweet(tweet))
    enriched.foreachPartition(send_partition)


# Send an individual partition to Kafka
def send_partition(iter):
    kafka_topic = "test"
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    for record in iter:
        producer.send(kafka_topic,json.dumps(record).encode('utf-8'))
    producer.close()



def enrichTweet(tweet):
    json_tweet = json.loads(tweet)
    tweet_text = str(json_tweet["text"])
    print("text: "+ tweet_text)
    json_tweet["sentiment"] = str(predict(tweet_text,classifier))
    return json.dumps(json_tweet)



#
#  MAIN APPLICATION
#

spark = SparkSession \
    .builder \
    .appName("Twitter Sentiment Analysis") \
    .getOrCreate()
sc = spark.sparkContext


classifier = joblib.load('./Twitter-Sentiment-Classifier/src/svmClassifier.pkl')
ssc = StreamingContext(sc, 300) #300 is the batch interval in seconds *5 minutes
IP = "localhost"
Port = 5555
lines = ssc.socketTextStream(IP, Port)

lines.foreachRDD( lambda rdd: process_to_file(rdd) )

# Start the Spark StreamingContext, and await process termination…
ssc.start()

ssc.awaitTermination()