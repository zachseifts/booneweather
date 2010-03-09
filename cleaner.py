#!/usr/bin/env python

import os
import private

class Cleaner(object):
    ''' Cleans various stuff around teh bot.'''

    def clean(self):
        self.delete_pickles()

    def delete_pickles(self):
        '''Removes the old pickle files.'''
        pickle_file = private.PICKLEFILE
        if os.path.exists(pickle_file):
            os.remove(pickle_file)

if __name__ == '__main__':
    cleaner = Cleaner()
    cleaner.delete_pickles()
    print os.path.dirname(os.path.abspath(__file__))

