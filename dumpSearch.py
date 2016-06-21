# -*- coding: utf-8 -*-

import twitter
from twitter import *


# ******************************************************************************************
# ** You need to register your app on Twitter and complete the following fields
# ****************************************************************************************
# auth = OAuth(
#     consumer_key='yourConsumerKey',
#     consumer_secret='yourConsumerSecret',
#     token='yourToken',
#     token_secret='yourTokenSecret'
# )

from authKeys import *


import csv, sys
import time as time2
import os
# import datetime
from datetime import time, date, datetime, tzinfo, timedelta


import urlparse
import json

from TwitterTimeParse import format_date
from DictUnicodeWriter import *


BASE = "dumps" # Base folder for output
query = u"selección Colombia"
fromDate = "2016-05-19"
toDate = "2016-06-16"

def extractMaxId(nextRes):
    parsed = urlparse.urlparse(nextRes)
    return int(urlparse.parse_qs(parsed.query)['max_id'][0])




def saveTweets(res, out):

    print "Saving %d tweets" % (len(res['statuses']))
    for t in res['statuses']:
        # print t
        out.write(json.dumps(t) + "\n")
        # print ".",
        # break



search = Twitter(auth=auth)
# stream = TwitterStream(auth=auth)

def downloadTweets():
    filename= query+"Tweets.dump"
    out = open(os.path.join(BASE,query,filename), "w")

    res = search.search.tweets(q=query,since=fromDate, until=toDate,count=100)
    while True:
        saveTweets(res, out)
        if 'next_results' in res['search_metadata'].keys():
            nextRes = res['search_metadata']['next_results']
            maxId = extractMaxId(nextRes)
            print "Got more results maxId="+str(maxId)
            print nextRes
            time2.sleep(1)
            print "requesting"
            # search = Twitter(auth=auth)
            res = search.search.tweets(max_id=maxId,q=query,since=fromDate, until=toDate,count=100,include_entities=1)
            # print res
        else:
            print "done"
            break


def processTweet(t, writer):
    pt = {}

    pt["tid"] = t['id_str'] if 'id_str' in t.keys() else t[u'id_str']
    pt["created"] = t['created_at'] if 'created_at' in t.keys() else t[u'created_at']
    pt["user"] = t['user']['screen_name'] if 'user' in t.keys() else t[u'user'][u'screen_name']
    pt["text"] = t['text'] if 'text' in t.keys() else t[u'text']
    # pt["text"] = t[u'retweeted_status'][u'text'] if (u'retweeted_status' in t.keys() or 'retweeted_status' in t.keys()) else pt["text"]
    pt["isRT"] = (u'retweeted_status' in t.keys() or 'retweeted_status' in t.keys())
    pt["isFav"] = t[u'favorited']
    pt["rtUser"] = t[u'retweeted_status'][u'user'][u'screen_name'] if (u'retweeted_status' in t.keys() or 'retweeted_status' in t.keys()) else None
    # pt["createdFmt"] = format_date(pt["created"]).strftime('%Y-%m-%d %H:%M:%S %Z')
    pt["createdFmt"] = format_date(pt["created"]).strftime('%Y-%m-%d %H:%M:%S')
    pt["createdRaw"] = format_date(pt["created"])
    pt["createdRaw2"] = datetime.now()
    pt["tweetByHandle"]  = False
    pt["handlesMatched"] = []
    pt["keywordsMatched"] = []
    # print pt
    writer.writerow(pt)


def extractTweets():
    print "Extracting tweets csv"
    f = open(os.path.join(BASE,query,query + "Tweets.dump"))

    fields = "tid,created,user,text,text,isRT,isFav,rtUser,createdFmt,createdRaw,createdRaw2,tweetByHandle,handlesMatched,keywordsMatched".split(",")

    csvFileName=query+"Tweets.csv"
    csvfile = open(os.path.join(BASE,query,csvFileName), 'w')
    writer=DictUnicodeWriter(csvfile, fields)
    writer.writeheader()

    for t in f:
        pt = json.loads(t)
        processTweet(pt, writer)
        # break


# downloadTweets()
extractTweets()
