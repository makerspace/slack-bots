import os

#TODO move to settings file
commandChar = '!'
argChar = ':'

class Slack:
    
    def __init__(self, slackMachine):
        self.slackMachinePlugin = slackMachine
        self.logChannel = self.slackMachinePlugin.find_channel_by_name(self.slackMachinePlugin.settings['SLACK_LOG_CHANNEL'])

    def sendMessage(self, msgToSend, msg, always_thread_except_dm = True):
        dm_message = msg.channel.is_im
        if not dm_message and (always_thread_except_dm or msg.in_thread or not msg.text[0] == commandChar):
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    def sendStatusMessage(self, msgToSend, msg=None):
        print(msgToSend) #TODO Print to log file?
        if msg != None:
            msg.reply(msgToSend, in_thread=True)
        self.slackMachinePlugin.say(self.logChannel, msgToSend)

    def sendDirectMessage(self, msgToSend, user):
        self.slackMachinePlugin.send_dm(user, msgToSend)

    def getArguments(self, msg):
        args = msg.text.split(argChar)[1:]
        args = [item.strip() for item in args]
        return args

    def getSlackUserByID(self, slackUsername): #TODO some exception when not found
        return self.slackMachinePlugin.users[slackUsername]

    def getSlackUserByName(self, slackUsername):
        allUsers = self.slackMachinePlugin.users
        for user in allUsers:
            if allUsers[user].name == slackUsername:
                return user
        raise RuntimeError('Slack user:'+slackUserName+' not found')
