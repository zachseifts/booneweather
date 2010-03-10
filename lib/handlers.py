import twitter

class DirectMessageHandler(object):
    ''' Handles direct messages '''

    def __init__(self, username, password):
        self.api = twitter.Api(username=username, password=password)
        self.get_messages()
        self.respond()
        self.clean()

    def get_messages(self):
        ''' Gets a list of the direct messages. '''
        self.messages = self.api.GetDirectMessages()

    def respond(self):
        ''' Responds to each direct message. '''
        for m in self.messages:
            message = 'wait, this works???? (not yet, but soon)'
            user = m.sender_screen_name
            self.api.PostDirectMessage(user, message)

    def clean(self):
        ''' Deletes the direct messages after they have been replied to.'''
        [self.api.DestroyDirectMessage(m.id) for m in self.messages]


