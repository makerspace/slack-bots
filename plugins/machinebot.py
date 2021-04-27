from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import respond_to, listen_to, process, on
import re, os

from base.slack import Slack
from utils.command_descriptions import Command, CommandDescriptions
from utils.bot_descriptions import Bot, BotDescriptions

class MachinePlugin(MachineBasePlugin):

    commands = CommandDescriptions()

    def init(self):
        self.bots = BotDescriptions()
        machineBot = Bot("machinebot", "har funktioner relaterat till status på spacets maskiner")
        self.bots.add(machineBot)

    def init_final(self):
    #@process('hello')
    #def start(self, event):
        self.slackUtil = Slack(self)
        self.slackUtil.sendStatusMessage("Machine plugin started.")

    command = Command('machinebot', 'Beskrivning av maskin botten')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutMachineBotQuestion(self, msg):
        msgToSend='Maskin botten används för status på spacets maskiner.'+"\nArgument delas upp med :\n"+str(self.commands) #TODO fix : so it is in a settings file
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('setstatus', 'Sätt status på en maskin', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def setStatusSlack(self, msg):
        msgToSend="Asdf"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('getstatus', 'Hämta status på en maskin', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def getStatusSlack(self, msg):
        msgToSend="Asdf"
        self.slackUtil.sendMessage(msgToSend, msg)

#TODO addMachine removeMachine
#TODO list broken machine all or for specific room
