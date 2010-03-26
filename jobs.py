#!/usr/bin/env python

import os
import inspect
import redis

from lib.objects import Weather
from lib.handlers import DirectMessageHandler

import private
from etc import config


class Jobs(object):
    ''' Jobs that are run by a cron job. 
    
    Be aware that every time you run this script it will make api calls
    to twitter. 
    '''

    def __init__(self, **kwargs):
        ''' Starts each job automatically.

        To create a new job, prefix the function with `job_` and it will
        be picked up by the parser.
        '''
        if not kwargs.get('no_auto_run'):
            [getattr(self, x)() for (x,y) in inspect.getmembers(self) if x.startswith('job_')]

    def job_update_weather(self):
        ''' Refreshes the redis set that contains all of the weather
        conditions.'''
        w = Weather()
        r = redis.Redis('localhost')
        r.set('weather:current:temp', w.temp)
        r.set('weather:current:cond', w.cond)
        r.set('weather:tomorrow:high', w.tom_high)
        r.set('weather:tomorrow:low', w.tom_low)

    def job_handle_direct_messages(self):
        ''' Handles sending and recieving direct messages. '''
        handler = DirectMessageHandler(private.USERNAME,
                                       private.PASSWORD)


if __name__ == '__main__':
    jobs = Jobs()

