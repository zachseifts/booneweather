#!/usr/bin/env python

''' @booneweather twitter bot.
'''

import os

from lib.objects import Weather, BooneWeather
import private


username = private.USERNAME
password = private.PASSWORD

if __name__ == '__main__':
    bw = BooneWeather(username=username, password=password)

