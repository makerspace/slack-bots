from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
from trello import TrelloClient
import re, os, mysql.connector

from utils.slackUtil import SlackUtil
import utils.regexFunctions as rFunc

class TrelloPlugin(MachineBasePlugin):

    def init(self):
        trelloApiKey = os.getenv('TRELLO_API_KEY')
        trelloApiSecret = os.getenv('TRELLO_API_SECRET')
        trelloTokenKey = os.getenv('TRELLO_TOKEN_KEY')
        trelloTokenSecret = os.getenv('TRELLO_TOKEN_SECRET')
        
        if trelloApiKey == None:
            raise RuntimeError('TRELLO_API_KEY not set') 
        if trelloApiSecret == None:
            raise RuntimeError('TRELLO_API_SECRET not set') 
        if trelloTokenKey == None:
            raise RuntimeError('TRELLO_TOKEN_KEY not set') 
        if trelloTokenSecret == None:
            raise RuntimeError('TRELLO_TOKEN_SECRET not set')

        self.trelloClient = TrelloClient(trelloApiKey, trelloApiSecret, trelloTokenKey, trelloTokenSecret)
        print('Connected with Trello')
        
        for board in self.trelloClient.list_boards():
            board.fetch()
            if self.settings['TRELLO_BOARD_URL'] == board.url:
                self.trelloBoard = board
                break

        print('Using trello board named '+self.trelloBoard.name+' with url: '+self.trelloBoard.url)
        
        for boardList in self.trelloBoard.all_lists():
            boardList.fetch()
            if self.settings['TRELLO_LIST_NEW_CARDS'] == boardList.name:
                self.trelloNewCardList = boardList
        
        print('Using trello list named '+self.trelloNewCardList.name)

    def init_final(self):
        self.slackUtil = SlackUtil(self)

    @listen_to(regex=rFunc.createRegEx('trello'))
    def aboutTrelloQuestion(self, msg):
        msgToSend='Spacets trello brädet med att-göra lista finns på: '+self.trelloBoard.url
        self.slackUtil.sendMessage(msgToSend, msg)
        
    @listen_to(regex=rFunc.createRegEx('trellobot'))
    def aboutTrelloBotQuestion(self, msg):
        msgToSend='Trello botten jobbar mot trello där spacet har att-göra listan.\n Brädet finns på: '+self.trelloBoard.url
        self.slackUtil.sendMessage(msgToSend, msg)

    @listen_to(regex=rFunc.createRegExWithArgument('addcard',1))
    def addCardSlack(self, msg):
        argList = self.slackUtil.getArguments(msg)
        cardName = argList[0]
        cardLabel = msg.channel.name
        
        self.trelloNewCardList.add_card(cardName, cardLabel, position='top')
        
        self.slackUtil.sendStatusMessage('Succesfully added card', msg)

#TODO complete card

#TODO assignme
#TODO assign
#TODO which cards are assigned to me
#TODO function to connect slack user with trello username

#TODO print to slack when card completed, added etc when its done in trello itself
