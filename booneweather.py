#!/usr/bin/env python

from random import choice
from urllib2 import HTTPError

import tweepy

from lib.objects import RedisConnector
from lib.objects import NoDataInRedis

from private import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

class Main(object):
    def __init__(self, ):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        self.update()

    def update(self):
        r = RedisConnector()
        temp = r.get('booneweather:current:temp')
        cond = r.get('booneweather:current:cond')
        tom_high = r.get('booneweather:tomorrow:high')
        tom_low = r.get('booneweather:tomorrow:low')
        if (temp and cond and tom_high and tom_low):
            tweet = 'Currently %s F and %s in %s. Tomorrow: high %s F, low: %s F #boone'
            name = choice('boonetana,booneville,boonetopia,booneberg'.split(','))
            self.tweet = tweet % (temp, cond, name, tom_high, tom_low)
            try:
                self.api.update_status(self.tweet)
            except HTTPError:
                # fail whale ftw
                pass
            except tweepy.error.TweepError:
                # duplicate tweet.
                pass
        else:
            raise NoDataInRedis



if __name__ == '__main__':
    Main()

