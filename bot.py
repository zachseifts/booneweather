#!/usr/bin/env python

''' @booneweather twitter bot.
'''

import os

from lib.objects import Weather, BooneWeather
import private


username = private.USERNAME
password = private.PASSWORD

if __name__ == '__main__':
    format = '%(asctime)s %(name)-25s %(levelname)-8s %(message)s'
    bw = BooneWeather(username=username, password=password)

