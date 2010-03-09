#!/usr/bin/env python

''' @booneweather twitter bot.
'''

import os
import logging

from lib.objects import Weather, BooneWeather
import private


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

