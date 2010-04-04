from datetime import datetime

import twitter
import redis
from urllib2 import HTTPError, URLError

class DirectMessageHandler(object):
    ''' Handles direct messages '''

    def __init__(self, username, password):
        self.api = twitter.Api(username=username, password=password)
        self.get_messages()
        self.respond()

    def log(self, level, user, message):
        ''' Creates a log entry everytime a dm is sent. '''
        now = datetime.now()
        r = redis.Redis('localhost')
        key = 'logs.booneweather:dm:sent'
        r.lpush(key, '%s | %s' % (now, user))
        key = 'logs:booneweather:dm:%s' % (user,)
        r.lpush(key, '%s | %s | %s' % (now, level, message))

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
        r = redis.Redis('localhost')
        temp = r.get('weather:current:temp')
        return 'heyo! the temp is %s F.' % (temp,)

