from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, process, on
import re, os

from base.slack import Slack
from base.calendar_parser import Calendar, Event
from utils.command_descriptions import Command, CommandDescriptions
from utils.bot_descriptions import Bot, BotDescriptions

class UtilPlugin(MachineBasePlugin):
  
    commands = CommandDescriptions()

    def init(self):
        self.bots = BotDescriptions()
        
        calendar_ical_url = os.getenv('BOT_CALENDAR_URL')
        if calendar_ical_url == None:
            raise RuntimeError('BOT_CALENDAR_URL not set')
        self.calendar = Calendar(calendar_ical_url)

    #def init_final(self):
    @process('hello')
    def start(self, event):
        self.slackUtil = Slack(self)
        self.slackUtil.sendStatusMessage("Util bot started.")

    command = Command('about','Information om bottarna')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutBotsQuestion(self, msg):
        msgToSend="Spacet har flera olika slack bottar.\n"+str(self.bots)
        self.slackUtil.sendMessage(msgToSend, msg)

    @process('member_joined_channel')
    def newMemberJoinChannel(self, event):
        if event['channel'] == self.find_channel_by_name("botlog").id: #TODO change to general when we are done
            self.slackUtil.sendStatusMessage("new member joined botlog")
            slackUser = self.slackUtil.getSlackUserByID(event['user'])
            #TODO slack machine need to be fixed for this to work
            #self.slackUtil.sendDirectMessage("Hej du gick med i botlog kanalen", slackUser)

    @process('channel_created')
    def channelCreated(self, event):
        msgToSend = "Slack channel created: " + event['channel']['name']
        self.slackUtil.sendStatusMessage(msgToSend)

    @process('channel_deleted')
    def channelCreated(self, event):
        msgToSend = "Slack channel deleted: " + event['channel']
        self.slackUtil.sendStatusMessage(msgToSend)
