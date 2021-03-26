from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
from trello import TrelloClient
import re, os, mysql.connector
import slackHelper as helper

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

    @listen_to(regex=helper.createRegEx('trello'))
    def aboutTrelloQuestion(self, msg):
        msgToSend='Spacets trello brädet med att-göra lista finns på: '+self.trelloBoard.url
        helper.sendMessage(msg, msgToSend)
        
    @listen_to(regex=helper.createRegEx('trellobot'))
    def aboutTrelloBotQuestion(self, msg):
        msgToSend='Trello botten jobbar mot trello där spacet har att-göra listan.\n Brädet finns på: '+self.trelloBoard.url
        helper.sendMessage(msg, msgToSend)

    @listen_to(regex=helper.createRegExWithArgument('addcard',1))
    def addCardSlack(self, msg): #TODO fix
        argList = helper.getArguments(msg)
        msgToSend=argList[0]
        helper.sendMessage(msg, msgToSend)

#TODO assignme
#TODO assign
#TODO which cards are assigned to me
#TODO function to connect slack user with trello username
