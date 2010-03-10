import pickle
import sys
from xml.dom.minidom import parseString
from random import choice

from httplib2 import Http
from tweetbot.bot import TwitterBot


sys.path.append('/Users/zach/dev/booneweather')
sys.path.append('/home/zach/bots/booneweather/src/booneweather')
from etc import config

class BadHTTPStatusException(Exception): pass


class Weather(object):
    ''' The current weather conditions by zip code.
    '''

    def __init__(self):
        self.temp, self.conds = self.conditions()

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
        temp = conditions.getAttribute('temp')
        cond = conditions.getAttribute('text').lower()
        return (temp, cond)


class BooneWeather(TwitterBot):
    ''' A twitter bot that tweets the current weather conditions in Boone, NC.
    '''

    def __init__(self, username, password):
        super(BooneWeather, self).__init__(username=username, password=password)
        # get the weather info from the pickle
        try:
            f = open(config.conditions, 'rb')
            self.weather = pickle.load(f)
            f.close()
            self.boone_names = 'boonetana,booneville,boonetopia,booneberg'.split(',')
            self.name = choice(self.boone_names)
            self.tweet = 'Currently %s F and %s in %s' % (self.weather.temp, self.weather.conds, self.name)
            self.post(self.tweet)
        except IOError:
            pass


