#!/usr/bin/env python

''' @booneweather twitter bot.
'''

import os
import logging
import pickle

from random import choice
from xml.dom.minidom import parseString

from httplib2 import Http
from tweetbot.bot import TwitterBot

import private


class BadHTTPStatusException(Exception): pass


class Weather(object):
    ''' The current weather conditions by zip code.
    '''

    def __init__(self):
        log = logging.getLogger('%s.Weather.__init__()' % (__file__))
        self.temp, self.conds = self.conditions()

    def conditions(self):
        ''' Returns the current conditions.'''
        log = logging.getLogger('%s.Weather.conditions()' % (__file__))
        WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
        h = Http('.cache')
        resp, content = h.request('http://weather.yahooapis.com/forecastrss?w=12769767')
        status = resp.get('status', None)
        if (not status and status is not None):
            raise BadHTTPStatusException, 'status returned is ' % (status)
        dom = parseString(content)
        conditions = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
        temp = conditions.getAttribute('temp')
        cond = conditions.getAttribute('text').lower()
        return (temp, cond)


class BooneWeather(TwitterBot):
    ''' A twitter bot that tweets the current weather conditions in Boone, NC.
    '''

    def __init__(self, username, password):
        log = logging.getLogger('%s.BooneWeather.__init__()' % (__file__))
        super(BooneWeather, self).__init__(username=username, password=password)
        self.weather = Weather()
        self.boone_names = 'boonetana,booneville,boonetopia,booneberg'.split(',')
        self.name = choice(self.boone_names)
        self.tweet = 'Currently %s F and %s in %s' % (self.weather.temp, self.weather.conds, self.name)
        self.post(self.tweet)


username = private.USERNAME
password = private.PASSWORD
pickle_file = private.PICKLEFILE

if __name__ == '__main__':
    format = '%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
    logging.basicConfig(level=private.LEVEL,
                        format=format,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=private.FILE,
                        filemode='w')
    bw = BooneWeather(username=username, password=password)

