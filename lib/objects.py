import sys
from xml.dom.minidom import parseString
from random import choice
from urllib2 import HTTPError

from httplib2 import Http
from tweetbot.bot import TwitterBot
from redis import Redis


class BadHTTPStatusException(Exception): pass
class NoDataInRedis(Exception): pass


class RedisConnector(object):
    ''' Wrapper for the Redis connection.
    '''

    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')
        self.redis = Redis(self.host)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value):
        return self.redis.set(key, value)

    def lpush(self, key, value):
        return self.redis.lpush(key,value)


class Weather(object):
    ''' The current weather conditions by yahoo area code.
    '''

    def __init__(self):
        self.conditions()

    def conditions(self):
        ''' Returns the current conditions.'''
        WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
        h = Http('.cache')
        resp, content = h.request('http://weather.yahooapis.com/forecastrss?w=12769767')
        status = resp.get('status', None)
        if (not status and status is not None):
            raise BadHTTPStatusException, 'status returned is ' % (status)
        dom = parseString(content)
        conditions = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
        tomorrow = dom.getElementsByTagNameNS(WEATHER_NS, 'forecast')[1]
        r = RedisConnector()
        r.set('weather:current:temp', conditions.getAttribute('temp'))
        r.set('weather:current:cond', conditions.getAttribute('text').lower())
        r.set('weather:tomorrow:high', tomorrow.getAttribute('high'))
        r.set('weather:tomorrow:low', tomorrow.getAttribute('low'))


class BooneWeather(TwitterBot):
    ''' A twitter bot that tweets the current weather conditions in Boone, NC.
    '''

    def __init__(self, username, password):
        super(BooneWeather, self).__init__(username=username, password=password)
        r = RedisConnector()
        temp = r.get('weather:current:temp')
        cond = r.get('weather:current:cond')
        tom_high = r.get('weather:tomorrow:high')
        tom_low = r.get('weather:tomorrow:low')
        if (temp and cond and tom_high and tom_low):
            tweet = 'Currently %s F and %s in %s. Tomorrow: high %s F, low: %s F'
            name = choice('boonetana,booneville,boonetopia,booneberg'.split(','))
            self.tweet = tweet % (temp, cond, name, tom_high, tom_low)
            try:
                self.post(self.tweet)
            except HTTPError:
                # fail whale ftw
                pass
        else:
            raise NoDataInRedis

