from sys import path
from datetime import datetime
from urllib2 import HTTPError, URLError

from twitter import Api

path.append('/Users/zach/dev/booneweather')
path.append('/home/bots/booneweather/src/booneweather')
from lib.objects import RedisConnector


class DirectMessageHandler(object):
    ''' Handles direct messages '''

    def __init__(self, username, password):
        self.api = Api(username=username, password=password)
        self.r = RedisConnector(host='localhost')
        self.get_messages()
        self.respond()

    def log(self, level, user, message):
        ''' Creates a log entry everytime a dm is sent. '''
        now = datetime.now()
        self.r.lpush('logs.booneweather:dm:sent', '%s | %s' % (now, user))
        self.r.lpush('logs:booneweather:dm:%s' % (user,),
                     '%s | %s | %s' % (now, level, message))

    def get_messages(self):
        ''' Gets a list of the direct messages. '''
        try:
            self.messages = self.api.GetDirectMessages()
        except HTTPError:
            pass
        except URLError:
            pass

    def respond(self):
        ''' Responds to each direct message and deletes it. '''
        for m in self.messages:
            command = m.text.split(' ')
            if len(command) > 2:
                message = self.command_help()
            if ['current', 'temp'] == command:
                message = self.command_current_temp() 
            elif ['current', 'precip'] == command:
                message = self.command_current_precip()
            else:
                message = self.command_help()
            user = m.sender_screen_name
            self.api.PostDirectMessage(user, message)
            self.log('debug', user, 'Sent DM: %s' % (message,))
            self.api.DestroyDirectMessage(m.id)

    def command_help(self):
        ''' Returns the help info to the user. '''
        return 'oh noes! commands: current temp, help'

    def command_current_temp(self):
        ''' Returns the current conditions to the user.'''
        temp = self.r.get('weather:current:temp')
        return 'heyo! the temp is %s F.' % (temp,)

    def command_current_precip(self):
        """Returns the current precipitation in boone!"""
        cond = self.r.get('weather:current:cond')
        return 'yo there! it\'s currently %s in boone' % (cond,)

