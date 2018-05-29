# -*- coding: utf-8 -*-
"""
Created on Tue May 29 11:10:36 2018

@author: sirdaniel
"""

import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import matplotlib


"# -- coding: utf-8 --"

def calctime(a):
    return time.time()-a

positive=0
negative=0
compound=0

count=0
initime=time.time()
plt.ion()

#import test

ckey= 'MfHOLQyQPV5KeqVvjxxzuYojE'
csecret= 'gx6oOowVOK62DOzCiCZKGe9xhZTrb2lBKM0TqubUolOTQ2Ha1Y'
atoken= '286628126-VsPQlCRcVTqX3k1li9DNIA73K5cXZiZOkjFWfKa8'
asecret= 'vdGsYcDRGNbWLVpcrcTtHSG7Vcz0CyWIkgWTOvn8zpd87'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

class listener(StreamListener):
    
    def on_data(self,data):
        global initime
        t=int(calctime(initime))
        all_data=json.loads(data)
        tweet=all_data["text"].encode("utf-8")
        #username=all_data["user"]["screen_name"]
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet))
        blob=TextBlob(tweet.strip())

        global positive
        global negative     
        global compound  
        global count
        
        count=count+1
        senti=0
        for sen in blob.sentences:
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity >= 0.3:
                positive=positive+sen.sentiment.polarity   
            else:
                negative=negative+sen.sentiment.polarity  
                
        compound=compound+senti        
        print count
        print tweet.strip()
        print senti
        print t
        print str(positive) + ' ' + str(negative) + ' ' + str(compound) 
        
    
        plt.axis([ 0, 500, -20,20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t] ,[negative],'ro',[t],[compound],'bo')
        plt.show()
        plt.pause(0.0001)
        if count==100:
            return False
        else:
            return True
        
    def on_error(self,status):
        print status



twitterStream=  Stream(auth, listener(count))
twitterStream.filter(track=["Buhari speech"])
