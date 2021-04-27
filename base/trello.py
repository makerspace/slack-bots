import os
from trello import Member as TrelloUser, TrelloClient

#TODO move to settings file
commandChar = '!'
argChar = ':'

class Trello:
    
    def __init__(self, boardUrl:str, listForNewCards:str):
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
            if boardUrl == board.url:
                self.trelloBoard = board
                break

        print('Using trello board named '+self.trelloBoard.name+' with url: '+self.trelloBoard.url)
        
        for boardList in self.trelloBoard.all_lists():
            boardList.fetch()
            if listForNewCards == boardList.name:
                self.trelloNewCardList = boardList
        
        print('Using trello list named '+self.trelloNewCardList.name)

    def getUserByName(self, trelloUsername):
        self.trelloBoard.fetch()
        allMembers = self.trelloBoard.all_members()

        print('qwe')
        print(allMembers)
        for member in allMembers:
            #member.fetch()
            #TODO is fetched required on member?
            if member.username == trelloUsername:
                return member
        raise RuntimeError('Trello user not found')

    def getUserByID(self, trelloID):
        self.trelloBoard.fetch()
        allMembers = self.trelloBoard.all_members()

        for member in allMembers:
            #TODO is fetched required on member?
            if member.id == trelloID:
                return member
        raise RuntimeError('Trello user not found')

    def getCard(self, card):
        self.trelloBoard.fetch()
        openCards = self.trelloBoard.get_cards(card_filter='open')
        for c in openCards:
            if c.name == card:
                return c
        raise RuntimeError('Card not found')

    def getCardInList(self, card): #TODO
        self.trelloBoard.fetch()
        openCards = self.trelloBoard.get_cards(card_filter='open')
        raise RuntimeError('Card not found')

    def addCard(self, cardName, desc=None, labels=None, due="null", position='top', assign=None, source=None, keep_from_source="all"):
        """Add a card to the active list
        :name: name for the card
        :labels: a list of label IDs to be added
        :due: due date for the card
        :source: card ID from which to clone from
        :position: position of the card in the list. Must be "top", "bottom" or a positive number.
        :desc: the description of the card
        :keep_from_source: can be used with source parameter. Can be "attachments", "checklists", "comments", "due", "labels", "members", "stickers" or "all".
        :return: the card
        """
        return self.trelloNewCardList.add_card(cardName, desc=desc, labels=labels, due=due, position=position, assign=assign, source=source, keep_from_source=keep_from_source)

    def closeCard(self, card):
        if isinstance(card, str):
            card = self.getCard(card)
        card.set_closed(True)

    def assign(self, card, trelloUser:TrelloUser):
        if isinstance(card, str):
            card = self.getCard(card)
        card.assign(TrelloUser.id)

    def unassign(self, card, trelloUser:TrelloUser):
        if isinstance(card, str):
            card = self.getCard(card)
        card.unassign(TrelloUser.id)

    def completeChecklistItem(self, trelloUser:TrelloUser):
        print('asdf') #TODO

    def completeChecklist(self, trelloUser:TrelloUser):
        print('asdf') #TODO
