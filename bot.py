#!/usr/bin/env python

''' @booneweather twitter bot.
'''

import os

from lib.objects import BooneWeather

import private


if __name__ == '__main__':
    bw = BooneWeather(username=private.USERNAME,
                      password=private.PASSWORD)

