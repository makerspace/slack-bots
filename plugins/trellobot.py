import re, os
from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import respond_to, listen_to, process, on
from trello import Member as TrelloUser
from machine.models.user import User as SlackUser

from base.slack import Slack
from base.trello import Trello
from utils.command_descriptions import Command, CommandDescriptions
from utils.bot_descriptions import Bot, BotDescriptions
from databases.slack_trello_database import SlackTrelloDB

class TrelloPlugin(MachineBasePlugin):

    commands = CommandDescriptions()

    def init(self):
        self.trello = Trello(self.settings['TRELLO_BOARD_URL'], self.settings['TRELLO_LIST_NEW_CARDS'])
        self.bots = BotDescriptions()
        trelloBot = Bot("trellobot", "har funktioner för att hantera kort på trello som används för spacets att-göra lista.")
        self.bots.add(trelloBot)

    #Hello event triggers when the connection with slack is established
    @process('hello')
    def start(self, event):
        self.slackUtil = Slack(self)
        self.slackTrelloDB = SlackTrelloDB(self.slackUtil, self.trello, self.settings['SLACK_TRELLO_USER_DB'], self.settings['SLACK_TRELLO_USER_TABLE'])
        if __debug__:
            self.slackUtil.sendStatusMessage("Trello plugin started.")

    command = Command('trellobot', 'Beskrivning av trello botten')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutTrelloBotQuestion(self, msg):
        msgToSend='Trello botten används för trello där spacet har att-göra listan. Brädet finns på: '+self.trello.trelloBoard.url+"\nArgument delas upp med :\n"+str(self.commands) #TODO fix : so it is in a settings file
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('trello', 'Länk till spacets trello bräde')
    commands.add(command)
    @listen_to(regex=command.regex)
    def aboutTrelloQuestion(self, msg):
        msgToSend='Spacets trello brädet med att-göra lista finns på: '+self.trello.trelloBoard.url
        self.slackUtil.sendMessage(msgToSend, msg)

    command = Command('addcard', 'Lägg till ett nytt kort på trello', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def addCardSlack(self, msg):
        argList = self.slackUtil.getArguments(msg)
        cardName = argList[0]
        cardLabel = msg.channel.name
        self.trello.addCard(cardName, cardLabel)
        self.slackUtil.sendStatusMessage('Succesfully added card', msg)

    command = Command('closecard', 'asdf',1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def completeCard(self, msg):
        argList = self.slackUtil.getArguments(msg)
        cardName = argList[0]
        self.trello.closeCard(cardName)
        self.slackUtil.sendStatusMessage('Succesfully completed card', msg)

    command = Command('trellouser', 'Länka ihop din slack användare med trello. Argumentet är användarnamnet på trello', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def connectSlackUserWithTrelloUser(self, msg):
        argList = self.slackUtil.getArguments(msg)
        slackUser = msg.sender
        trelloUsername = argList[0]
        try:
            trelloUser = self.trello.getUserByName(trelloUsername)
        except:
            self.slackUtil.sendStatusMessage("Can not find trello user: "+trelloUsername, msg)
            return

        try:
            self.slackTrelloDB.addUser(slackUser, trelloUser)
        except:
            self.slackUtil.sendStatusMessage("Failed to add to database", msg)
            return
        self.slackUtil.sendStatusMessage("Succesfully stored slack, trello user association", msg)

#TODO unlink trellouser function 

    def _assign(self, cardName, slackUser):
        if isinstance(slackUser, str):
            try:
                slackUser = self.slackUtil.getUserByName(slackUser)
            except:
                self.slackUtil.sendStatusMessage("Can not find slack user: "+slackUser, msg)
                return

        try:
            trelloUser = self.slackTrelloDB.getTrelloUser(slackUser)
        except:
            self.slackUtil.sendStatusMessage("Can not find corresponding trello user in database", msg)
            return

        self.trello.assign(cardName, trelloUser)
        self.slackUtil.sendStatusMessage('Succesfully assigned card', msg)

    command = Command('assign', 'Tilldela någon det specifierade kort', 2)
    commands.add(command)
    @listen_to(regex=command.regex)
    def assign(self, msg):
        argList = self.slackUtil.getArguments(msg)
        cardName = argList[0]
        slackUser = argList[1]
        self._assign(cardName, slackUser)

    command = Command('assignme', 'Tilldela dig det specifierade kort', 1)
    commands.add(command)
    @listen_to(regex=command.regex)
    def assignMe(self, msg):
        argList = self.slackUtil.getArguments(msg)
        cardName = argList[0]
        slackUser = msg.sender
        self._assign(cardName, slackUser)

#TODO unassignme and unassign

    command = Command('mycards', 'Listar öppna kort som du har blivit tilldelad')
    commands.add(command)
    @listen_to(regex=command.regex)
    def myCards(self, msg):
        slackUser = msg.sender
        #TODO remember to only get the open cards

#TODO all open cards, put it in a general def?
#TODO all open cards with the channel as label, put it in a general def?

#TODO complte checklist items and whole checklist

#TODO use webhook or such to:
#TODO print to slack when card completed, added etc
#TODO print to the corresponding slack channel when card is commented, attachted to etc
