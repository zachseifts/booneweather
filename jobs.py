#!/usr/bin/env python

import os
import inspect
import pickle

from lib.objects import Weather

from etc import config


class Jobs(object):
    ''' Things that do stuff.'''

    def __init__(self):
        self.runner()

    def runner(self):
        ''' Runs jobs added to this object.

            To register a job create a method that starts with `job_` your action.
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

