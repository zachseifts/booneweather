#!/usr/bin/env python

import os
import inspect

from lib.objects import Weather


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
        ''' Refreshes the weather. '''
        Weather()


if __name__ == '__main__':
    jobs = Jobs()

