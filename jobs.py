#!/usr/bin/env python

import os
import inspect
import pickle

from lib.objects import Weather

from etc import config


class Jobs(object):
    ''' Jobs that are run by a cron job. 
    
    Be aware that every time you run this script it will make api calls
    to twitter. 
    '''

    def __init__(self):
        ''' Starts each job automatically.

        To create a new job, prefix the function with `job_` and it will
        be picked up by the parser.
        '''
        [getattr(self, x)() for (x,y) in inspect.getmembers(self) if x.startswith('job_')]

    def job_update_weather(self):
        ''' Refreshes the pickle object that contains all of the weather
        conditions.'''
        if os.path.exists(config.conditions):
            os.remove(config.conditions)
        w = Weather()
        f = open(config.conditions, 'w')
        pickle.dump(w, f)
        f.close()


if __name__ == '__main__':
    jobs = Jobs()

