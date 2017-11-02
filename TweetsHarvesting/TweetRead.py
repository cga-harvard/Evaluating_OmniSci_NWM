#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:13:54 2017

@author: ellenk
"""

# TweetRead.py

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
from twitter import *
import os
import sys
import time
import json
 
consumer_key    = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token    = os.environ['TWITTER_ACCESS_TOKEN']
access_secret   = os.environ['TWITTER_ACCESS_SECRET']
 



class TweetsListener(StreamListener):
 
    def __init__(self, csocket):
        self.client_socket = csocket
 
    def on_data(self, data):
        try:
           # print json.dumps(data.split('\n'),sort_keys=True,indent=4, separators=(',', ': '))
            print(data.split('\n'))

            self.client_socket.send(data.encode('utf-8'))

            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True


def sendData(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(locations=[-74,40,-73,41])




 
if __name__ == "__main__":
    s = socket.socket()     # Create a socket object
    host = "localhost"      # Get local machine name
    port = 5555             # Reserve a port for your service.
    s.bind((host, port))    # Bind to the port
 
    print("Listening on port: %s" % str(port))
 
    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.
    
    print(" type(c): " + str(type(c)))
    print( "Received request from: " + str( addr ) )
 
    try:
        sendData( c )
    finally:
        s.close()