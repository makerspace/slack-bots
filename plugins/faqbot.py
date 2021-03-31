from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, process, on
import re

from utils.slack import Slack
from utils.command_descriptions import Command, CommandDescriptions

class AnswerFAQPlugin(MachineBasePlugin):
   
    #TODO use message payload for the weblinks?

    commands = CommandDescriptions()

    #def init(self):

    def init_final(self):
        self.slackUtil = Slack(self)
        #self.slackUtil.sendStatusMessage("FAQ bot started.")

    command = Command('faqbot', 'Beskrivning av faq botten')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor\n Argument delas upp med :\n"+str(self.commands) #TODO fix : so it is in a file
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('about','Information om bottarna')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutBotsQuestion(self, msg): #TODO
        msgToSend="Vi har lite olika slack bottar.\nFAQ bot: "+'!'+"faqbot" #TODO move ! to a settings file
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('faq','Länk till Makerspace FAQ')
    commands.add(command)
    @listen_to(regex=command.regex)
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('nyckel','Information om nyckelutlämningar')
    commands.add(command)
    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=command.regex)
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)" #TODO
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('box','Information om hur det fungerar med labblåda')
    commands.add(command)
    @listen_to(regex=command.regex)
    def boxQuestion(self, msg):
        msgToSend="Maximala måtten för labblåda är ca 50 x 39 x 26 cm. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Makerspace_FAQ#F%C3%B6rvaring"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('wiki','Länkar till wiki sidan som motsvarar argumentet', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def wikiQuestion(self, msg):
        argList = self.slackUtil.getArguments(msg)
        msgToSend="https://wiki.makerspace.se/"+argList[0]
        self.slackUtil.sendMessage(msgToSend, msg)

    @process('member_joined_channel')
    def newMemberJoinChannel(self, event):
        if event['channel'] == self.find_channel_by_name("botlog").id: #TODO change to general when we are done
            self.slackUtil.sendStatusMessage("new member joined botlog")
            slackUser = self.slackUtil.getSlackUserByID(event['user'])
            #TODO slack machine need to be fixed for this to work
            #self.slackUtil.sendDirectMessage("Hej du gick med i botlog kanalen", slackUser)
