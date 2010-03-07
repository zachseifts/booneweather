#!/usr/bin/env python

import os
from ConfigParser import ConfigParser

class Cleaner(object):
    ''' Cleans various stuff around teh bot.'''

    def clean(self):
        self.delete_pickles()

    def delete_pickles(self):
        '''Removes the old pickle files.'''
        pickle_file = config.get('cache', 'picklefile')
        if os.path.exists(pickle_file):
            os.remove(pickle_file)


config = ConfigParser()
config.read('settings.conf')

if __name__ == '__main__':
    cleaner = Cleaner()
    cleaner.delete_pickles()

