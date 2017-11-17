# This code harvest Geotweets and then saves as .tsv
# Author:tmostak
# Modified by: Devika Kakkar
# Modified on: October 16, 2017

import time
from datetime import datetime
#from urllib2 import URLError
import sys
import subprocess
import math
import threading
import os 
import imp
import csv
from datetime import datetime
import json
import os
import requests  # http://docs.python-requests.org/en/master/
#import datetime as dt
#from kafka import KafkaProducer
#from kafka import KafkaConsumer
#from kafka import KafkaProducer
#from kafka.errors import KafkaError


from twitter import *

# Convert

def conv4326To900913 (lonLat): #expects tuple of x,y
    outCoords = [0.0] * 2 
    outCoords[0] = lonLat[0] * 111319.490778
    outCoords[1] = 57.295779513083 * math.log(math.tan(.0087266462599717*lonLat[1] + .78539816339745)) 
    outCoords[1] *= 111319.490778
    return outCoords

# Authorization credentials

def authenticateUser (userName, appInfo):
    #print >> sys.stderr, 'Authenticating user ' 
    if (userName == 'databases4life'):
        oauthToken_user_1 = '1173337286-rhxiLu2YWTmWuKrlwYL6qcBvO5pReLzxli3gfGS'
        oauthSecret_user_1 = 'cuTom9AH4rEaYG2QdYN202LBhjzHe5Ex9F29cizzQ'
        return oauthToken_user_1, oauthSecret_user_1
    
    elif (userName == 'gamalabdalwahid'):
        oauthToken_user_2 = '568766576-9OeLy4k31jH0xGsq9FtnvGYZZBnZUs7oDxTLoQIm'
        oauthSecret_user_2 =  '3XrsGv3OYkwhaoy2co77B4Xk5Dk7gVN0DUWACRmPBY'
        return oauthToken_user_2, oauthSecret_user_2
        
    elif (userName == 'Velos_MapD'):
        oauthToken_user_3 = '964655989-DFtRLIqlYtjLIGoolNjLptmpMgTUCkU1u6eUaqBN'
        oauthSecret_user_3 =  '6tR1iOZNUMVyMZdB7AmJ2EswtXapwkN0sI5PkbiYzA'
        return oauthToken_user_3, oauthSecret_user_3
        

    elif (userName == 'kedahek'):
        oauthToken_user_4 = 'Dw7MVHD4v4P0Kts1lbwWvv7AAZin7XJEctHcKJ08k'
        oauthSecret_user_4 =  'Dw7MVHD4v4P0Kts1lbwWvv7AAZin7XJEctHcKJ08k'
        return oauthToken_user_4, oauthSecret_user_4
        

    elif (userName == 'tmostak'):
        oauthToken_user_5 = '1173286686-4xkTwHF3FvnSKGTQHOjhuP1spmZBx1ot7y639oI'
        oauthSecret_user_5 =  'zou9RZIidZpZ2Y3Rgbac4Ockc8cIrMPyF3ROUBiCetk'
        return oauthToken_user_5, oauthSecret_user_5
        
# The Harvester class

class Harvester (threading.Thread):
    maxErrors = 10
    def __init__(self, username, harvName, boundingBox, appInfo): #boundingBox is tuple in form (minX, minY, maxX, maxY)
        super(Harvester,self).__init__()
        self.username = username
        self.harvName = harvName
        self.boundingBox = boundingBox # should be tuple of len 4
        self.location = str(self.boundingBox[0]) + "," + str(self.boundingBox[1]) + "," +  str(self.boundingBox[2]) + "," + str(self.boundingBox[3])
        self.daemon = True
        self.appInfo = appInfo
        self.token, self.secret = authenticateUser(self.username, self.appInfo) 

    def run(self):
        twitterStream = TwitterStream(auth=OAuth(self.token, self.secret, self.appInfo["key"], self.appInfo["secret"]))
        #print >> sys.stderr, 'Filtering the public timeline for '  
        streamIt = twitterStream.statuses.filter(locations=self.location)
        errorCount = 0
        
        dirname = '/home/ubuntu/geo_tweets_harvester/data/'
        while errorCount < 10: 
            try:
                for tweet in streamIt:
                        if tweet.get('text'):
                            date= datetime.now().strftime('%Y-%m-%d %H')
                
        
                            #print("Date is", date)
                            year = date[:4]
                            month= date[5:7]
                            day= date[8:10]
                            hour = date[11:13]
                            #print(year)
                            #print(month)
                            #print(day)
                            #print(hour)
                            DHG = year + '_' + month + '_' + day + '_' + hour
                            fname = "geo_tweets_hour_" + DHG + ".tsv"
                            file_exists = os.path.isfile(os.path.join(dirname, fname))
                            #print(fname, file_exists)

                            f = open(os.path.join(dirname, fname),'a',encoding='utf-8')
                            fieldnames = ['tweet_id', 'time','lat','lon','goog_x','goog_y','sender_id','sender_name','source','reply_to_user_id','reply_to_tweet_id','place_id','tweet_text','lang']
                            writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter='\t')

                            if not file_exists:
                                writer.writeheader()  # file doesn't exist yet, write a header
                                #print ('after writing header')

                            #print("Date is", date)
                            coordinates = tweet.get('coordinates')
                            #print("Tweet corrdinate", coordinates)
                            if (coordinates != None):
                                    if tweet.get('text'):
                                        tweetText = tweet.get('text')
                                        tweetText = tweetText.replace('\n', ' ').replace('\t', ' ')
                                    tweet_id = tweet.get('id')
                                    rawTime = tweet['created_at']
                                    structTime = time.strptime(rawTime, "%a %b %d %H:%M:%S +0000 %Y")
                                    stringTime = time.strftime("%Y-%m-%d %H:%M:%S", structTime)
                                    #time = stringTime
                                    geo = tweet.get('geo')
                                    if geo != None and geo != '':
                                        lat = geo['coordinates'][0]
                                        lon = geo['coordinates'][1]                                                
                                    
                                    place = tweet.get('place')
                                    if place == None:
                                        place = {}
                                    googCoords = [None] * 2
                                    if lat != None and lon != None:
                                        try:
                                            googCoords = conv4326To900913((lon, lat))
                                        except Exception as x:
                                            pass # most likely b/c of math domain error
                                    source = tweet.get('source')
                                    if source != None:
                                        if source.count('<') == 2 and source.count('>') == 2: 
                                            startInner = source.find('>') + 1
                                            endInner = source.find('<', startInner)
                                            source = source[startInner:endInner]
                                        
                                    user = tweet['user']
                                    goog_x = googCoords[0]
                                    goog_y = googCoords[1]
                                    sender_id = user.get('id')
                                    sender_name = user.get('screen_name')
                                    reply_to_user_id = tweet.get('in_reply_to_user_id')
                                    reply_to_tweet_id = tweet.get('in_reply_to_status_id')
                                    place_id = place.get('id', '')
                                    tweet_text = tweetText
                                    lang= tweet.get('lang')
                                    #print(tweet_id, stringTime,lat,lon,goog_x, goog_y,sender_id,sender_name,source, reply_to_user_id, reply_to_tweet_id,place_id, tweet_text, lang)
                                    writer.writerow({'tweet_id': (tweet_id), 'time': (stringTime), 'lat':(lat),'lon':(lon),'goog_x':(goog_x),'goog_y':(goog_y),'sender_id':(sender_id),'sender_name':(sender_name),'source':(source),'reply_to_user_id':(reply_to_user_id),'reply_to_tweet_id':(reply_to_tweet_id),'place_id':(place_id),'tweet_text':(tweet_text),'lang':(lang)})
                                    #packed = msgpack.packb(tweet)
                                    #result = producer.send(os.environ["TWEET_TOPIC"],tweet)
                                    #md = result.get()
                                    #print("send() - %s" % str(md))                                

            except Exception as x:
                print ("Disconnected from Twitter: ",x)
                errorCount += 1
                time.sleep((2 * errorCount) ** 2 ) #exponentially back off
                sys.exc_clear()

            f.close() 
# Kafka Producer
#time.sleep(10)

#producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_HOST_PORT"],compression_type='lz4',acks=1,retries=30,linger_ms=100,retry_backoff_ms=1000,value_serializer=msgpack.dumps)
#producer = KafkaProducer(bootstrap_servers=os.environ["KAFKA_HOST_PORT"],compression_type=os.environ["COMPRESSION_TYPE"],acks= int(os.environ["ACKS"]), retries=int(os.environ["RETRIES"]),linger_ms=int(os.environ["LINGER_MS"]),retry_backoff_ms=int(os.environ["RETRY_BACKOFF_MS"]),value_serializer=msgpack.dumps)   


def main():
    appParams = {}
    userParams = []
    try:
        # App parameters
        appParams["name"] = 'Twerld'
        appParams["key"] = 'rIg8zjOpPcvGgWbteJYQ'
        appParams["secret"] = 'nXXc7wLxH7ONCNFEDrpNW7T0qGMkpUQfoLUXNhG1to'

        #Bounding boxes
        bounding_box_1 = 'NWW,databases4life,-180,15,-92,90'
        lyst_bb_1 = bounding_box_1.split(',')

        bounding_box_2 = 'NWE,gamalabdalwahid,-92,15,-30,90'
        lyst_bb_2 = bounding_box_2.split(',')

        bounding_box_3 = 'SW,Velos_MapD,-180,-90,-30,15'
        lyst_bb_3 = bounding_box_3.split(',')

        bounding_box_4 = 'EW,kedahek,-30,-90,60,90'
        lyst_bb_4 = bounding_box_4.split(',')

        bounding_box_5 = 'EE,tmostak,60,-90,180,90'
        lyst_bb_5 = bounding_box_5.split(',')


       # User parameters
        userParams=[[lyst_bb_1[0], lyst_bb_1[1], lyst_bb_1[2], lyst_bb_1[3], lyst_bb_1[4], lyst_bb_1[5]], [lyst_bb_2[0], lyst_bb_2[1], lyst_bb_2[2], lyst_bb_2[3], lyst_bb_2[4], lyst_bb_2[5]], [lyst_bb_3[0], lyst_bb_3[1], lyst_bb_3[2], lyst_bb_3[3], lyst_bb_3[4], lyst_bb_3[5]], [lyst_bb_1[0], lyst_bb_4[1], lyst_bb_4[2], lyst_bb_4[3], lyst_bb_4[4], lyst_bb_4[5]],[lyst_bb_5[0], lyst_bb_5[1], lyst_bb_5[2], lyst_bb_5[3], lyst_bb_5[4], lyst_bb_5[5]]]
        
    except Exception as x:
        #print x
        sys.exit(1)
    harvs = []
    for p in userParams:
       harvs.append(Harvester(p[1], p[0], (p[2], p[3], p[4], p[5]), appParams)) 

    numHarvs = len(harvs)
 
    for h in harvs:
        h.start()
        
    while len(harvs) > 0: 
        try:
            for h in range(numHarvs):
                harvs[h].join(1)
                if harvs[h].isAlive() == False:
                    harvs[h] = Harvester(userParams[h][1], userParams[h][0], (userParams[h][2], userParams[h][3], userParams[h][4], userParams[h][5]), appParams)
                    harvs[h].start()
        except KeyboardInterrupt: #allows us to cntl-c
            #producer.flush()
            #producer.close()
            sys.exit(2)
            
    
# Calling name    
if __name__ == "__main__":
    main()
