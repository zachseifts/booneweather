#!/usr/bin/env python

''' @booneweather twitter bot.
'''

import logging
from ConfigParser import ConfigParser

from random import choice
from xml.dom.minidom import parseString

from tweetbot.bot import TwitterBot
from httplib2 import Http


class Weather(object):
    ''' The current weather conditions by zip code.
    '''

    def __init__(self):
        log = logging.getLogger('%s.Weather.__init__()' % (__file__))
        self.temp, self.conds = self.conditions()

    def conditions(self):
        ''' Returns the current conditions.'''
        log = logging.getLogger('%s.Weather.conditions()' % (__file__))
        h = Http('.cache')
        WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
        resp, content = h.request('http://weather.yahooapis.com/forecastrss?w=12769767')
        status = resp.get('status', None)
        if (status and status is not None):
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


if __name__ == '__main__':
    config = ConfigParser()
    config.read('settings.conf')
    username=config.get('twitter', 'username')
    password=config.get('twitter', 'password')
    format = '%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
    logging.basicConfig(level=config.get('logging', 'level'),
                        format=format,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=config.get('logging', 'file'),
                        filemode='w')
    bw = BooneWeather(username=username, password=password)

