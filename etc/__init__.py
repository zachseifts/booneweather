import os
import tempfile

class Singleton(type):
    ''' Singleton pattern from stackoverflow.
    http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python/33201#33201
    '''

    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.instance


class Config(object):
    ''' A configuration object.

    '''
    __metaclass__ = Singleton

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.conds_file = 'conditions.pkl'
        self.conditions = os.path.join(self.temp_dir, self.conds_file)


config = Config()

