import twitter

class DirectMessageHandler(object):
    ''' Handles direct messages '''

    def __init__(self, username, password):
        self.api = twitter.Api(username=username, password=password)
        self.get_messages()
        self.respond()

    def get_messages(self):
        ''' Gets a list of the direct messages. '''
        self.messages = self.api.GetDirectMessages()

    def respond(self):
        ''' Responds to each direct message and deletes it. '''
        for m in self.messages:
            message = 'wait, this works???? (not yet, but soon)'
            user = m.sender_screen_name
            self.api.PostDirectMessage(user, message)
            self.api.DestroyDirectMessage(m.id)

