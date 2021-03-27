import os

commandChar = '!'
argChar = ':'

class SlackUtil:
    
    def __init__(self, slackMachine):
        self.slackMachinePlugin = slackMachine
        self.logChannel = self.slackMachinePlugin.find_channel_by_name(self.slackMachinePlugin.settings['SLACK_LOG_CHANNEL'])

    def sendMessage(self, msgToSend, msg):
        if msg.in_thread or not msg.text[0] == commandChar:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    def sendStatusMessage(self, msgToSend, msg=None):
        print(msgToSend) #TODO Print to log file?
        if msg != None:
            msg.reply(msgToSend, in_thread=True)
        self.slackMachinePlugin.say(self.logChannel, msgToSend)

    def getArguments(self, msg):
        args = msg.text.split(argChar)[1:]
        [item.strip() for item in args]
        return args
