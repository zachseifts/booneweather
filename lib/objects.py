import sys
from xml.dom.minidom import parseString
from random import choice

from httplib2 import Http
from tweetbot.bot import TwitterBot
import redis


sys.path.append('/Users/zach/dev/booneweather')
from etc import config

class BadHTTPStatusException(Exception): pass
class NoWeatherInRedis(Exception): pass


class Weather(object):
    ''' The current weather conditions by zip code.
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
        self.temp = conditions.getAttribute('temp')
        self.cond = conditions.getAttribute('text').lower()
        self.tom_cond = tomorrow.getAttribute('text').lower()
        self.tom_high = tomorrow.getAttribute('high')
        self.tom_low = tomorrow.getAttribute('low')


class BooneWeather(TwitterBot):
    ''' A twitter bot that tweets the current weather conditions in Boone, NC.
    '''

    def __init__(self, username, password):
        super(BooneWeather, self).__init__(username=username, password=password)
        r = redis.Redis()
        temp = r.get('weather:current:temp')
        cond = r.get('weather:current:cond')
        tom_high = r.get('weather:tomorrow:high')
        tom_low = r.get('weather:tomorrow:low')
        if (temp or cond or tom_high or tom_low):
            tweet = 'Currently %s F and %s in %s. Tomorrow: high %s F, low: %s F'
            name = choice('boonetana,booneville,boonetopia,booneberg'.split(','))
            self.tweet = tweet % (temp, cond, name, tom_high, tom_low)
            self.post(self.tweet)

