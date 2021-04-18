from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, process, on
import re, os

from base.slack import Slack
from base.calendar_parser import Calendar, Event
from utils.command_descriptions import Command, CommandDescriptions
from utils.bot_descriptions import Bot, BotDescriptions

class AnswerFAQPlugin(MachineBasePlugin):
   
    #TODO use message payload for the weblinks?

    commands = CommandDescriptions()

    def init(self):
        self.bots = BotDescriptions()
        faqBot = Bot("faqbot", "svarar på diverse frågor")
        self.bots.add(faqBot)
        
        calendar_ical_url = os.getenv('BOT_CALENDAR_URL')
        if calendar_ical_url == None:
            raise RuntimeError('BOT_CALENDAR_URL not set')
        self.calendar = Calendar(calendar_ical_url)

    #def init_final(self):
    @process('hello')
    def start(self, event):
        self.slackUtil = Slack(self)
        self.slackUtil.sendStatusMessage("FAQ bot started.")

    command = Command('faqbot', 'Beskrivning av faq botten')
    commands.add(command)
    @respond_to(regex=command.regex)
    @listen_to(regex=command.regex)
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor\nArgument delas upp med :\n"+str(self.commands) #TODO fix : so it is in a settings file
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
        event_nyckel = self.calendar.find_event('nyckelutlämning')
        msgToSend = "Nyckelutlämningar sker just nu mer sporadiskt pga pandemin och det är endast tidsbokning som gäller vid varje tillfälle."
        if event_nyckel == None:
            msgToSend += "\n"+"Det finns ingen planerad nyckelutläming."
        else:
            msgToSend += "\n"+"Nästa utlämning är " + event_nyckel.start_time.strftime("%d/%m, %H:%M")
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('box','Information om hur det fungerar med labblåda')
    commands.add(command)
    @listen_to(regex=command.regex)
    def boxQuestion(self, msg):
        msgToSend="Labblådan ska vara SmartStore Classic 31, den säljs tex av Clas Ohlsson och Jysk. Tänk på att man inte får förvara lithiumbatterier för radiostyrt på spacet pga brandrisken. Kemikalier ska förvaras kemiskåpet, ej i lådan. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Medlems_F%C3%B6rvaring"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('sopor','Information om sophantering')
    commands.add(command)
    @listen_to(regex=command.regex)
    def garbageQuestion(self, msg):
        msgToSend="Nyckelkortet till soprummet finns i städskrubben. Soprummet ligger på lastkajen bakom huset. Mer info och karta till soprummet finns på: https://wiki.makerspace.se/Sophantering"
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('wiki','Länkar till wiki sidan som motsvarar argumentet', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def wikiQuestion(self, msg):
        argList = self.slackUtil.getArguments(msg)
        msgToSend="https://wiki.makerspace.se/"+argList[0]
        self.slackUtil.sendMessage(msgToSend, msg)

#TODO inköpsansvariga
#TODO kurser/workshops med kalender grej
#TODO kurser/workshop faq/info

