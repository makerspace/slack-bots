from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import respond_to, listen_to, process, on
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

    #Hello event triggers when the connection with slack is established
    if __debug__:
        @process('hello')
        def start(self, event):
            self.slackUtil = Slack(self)
            self.slackUtil.sendStatusMessage("Util plugin started.")

    command = Command('about','Information om botten', aliases=['help'])
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutBotsQuestion(self, msg):
        msgToSend="Spacet har en slack bott med olika funktioner.\n"+str(self.bots)
        self.slackUtil.sendMessage(msgToSend, msg)

    @process('member_joined_channel')
    def newMemberJoinChannel(self, event):
        if event['channel'] == self.find_channel_by_name("general").id:
            self.slackUtil.sendStatusMessage("New member joined botlog")
            slackUser = self.slackUtil.getSlackUserByID(event['user'])
            msgToSend = "Hej välkomen till Stocholm Makerspaces slack. Missa inte att lägga till kanaler som du vill följa (rum, maskiner och intresseområden). #events används för att annonsera saker som händer (nyckelsynkroniseringar, workshops, etc.).\n"
            msgToSend += "Det här meddelandet är ifrån en bot som bland annat kan svara på vanliga frågor. Testa tex att skriva !faqbot i den här chatten med botten.\n" #TODO ! to settings file
            msgToSend += "För generell information om botten använd !about"
            #self.slackUtil.sendDirectMessage(msgToSend, slackUser)

    @process('channel_created')
    def channelCreated(self, event):
        msgToSend = "Slack channel created: " + event['channel']['name']
        self.slackUtil.sendStatusMessage(msgToSend)

    @process('channel_deleted')
    def channelCreated(self, event):
        msgToSend = "Slack channel deleted: " + event['channel']
        self.slackUtil.sendStatusMessage(msgToSend)
