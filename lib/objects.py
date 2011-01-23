import sys
from xml.dom.minidom import parseString
from random import choice
from urllib2 import HTTPError

from httplib2 import Http
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
    ''' The current conditions as Yahoo Weather and Weather Underground see them.
    '''

    def __init__(self, **kwargs):
        self.r = kwargs.get('r', RedisConnector())
        self.h = kwargs.get('h', Http('.cache'))
        self.yahoo_url = kwargs.get('yahoo_url', 'http://weather.yahooapis.com/forecastrss?w=12769767')
        self.wu_url = kwargs.get('wu_url', 'http://rss.wunderground.com/auto/rss_full/NC/Boone.xml?units=english')
        self.get_wu_weather()
        self.get_yahoo_weather()

    def get_feed(self, url):
        ''' Gets a feed and parses it.
        '''
        resp, content = self.h.request(url)
        status = resp.get('status', None)
        if (not status and status is not None):
            raise BadHTTPStatusException, 'status returned is ' % (status)
        dom = parseString(content)
        return resp, content, dom

    def get_yahoo_weather(self):
        ''' Gets the current conditions from Yahoo
        '''
        WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
        resp, content, dom = self.get_feed(self.yahoo_url)
        conditions = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
        tomorrow = dom.getElementsByTagNameNS(WEATHER_NS, 'forecast')[1]
        self.r.set('booneweather:tomorrow:high', tomorrow.getAttribute('high'))
        self.r.set('booneweather:tomorrow:low', tomorrow.getAttribute('low'))

    def get_wu_weather(self):
        ''' Gets the current conditions from Weather Underground
        '''
        resp, content, dom = self.get_feed(self.wu_url)
        conditions = dom.getElementsByTagName('item')[0].getElementsByTagName('description')[0].firstChild.toxml()[9:]
        conditions = conditions.split('<img')[0].split('|')
        self.r.set('booneweather:current:temp', conditions[0].split(': ')[1].split('&')[0].strip())
        self.r.set('booneweather:current:cond', conditions[3].split(': ')[1].split('&')[0].lower().strip())
        self.r.set('booneweather:current:wind_direction', conditions[4].split(': ')[1].split('&')[0].strip())
        self.r.set('booneweather:current:wind_speed', conditions[5].split(': ')[1].split('&')[0].strip())


