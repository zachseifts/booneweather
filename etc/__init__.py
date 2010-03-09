import os
import tempfile

class Config(object):
    ''' A configuration object.

    Should be a singleton.
    '''

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.conds_file = 'conditions.pkl'
        self.conditions = os.path.join(self.temp_dir, self.conds_file)

config = Config()
