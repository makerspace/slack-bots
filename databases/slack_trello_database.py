import os, mysql.connector
from trello import Member as TrelloUser
from machine.models.user import User as SlackUser

from utils.slack import Slack
from utils.trello import Trello

#TODO move to settings file
database_name = 'slack_trello'
table_name = 'users'

class SlackTrelloDB():

    def _init_(slack:Slack, trello:Trello):
        self._slack = slack
        self._trello= trello
        
        dbUser = os.getenv('MYSQL_USER')
        dbPassword = os.getenv('MYSQL_PASSWORD')
        if dbUser == None:
            raise RuntimeError('MYSQL_USER not set')
        if dbPassword == None:
            raise RuntimeError('MYSQL_PASSWORD not set') 
        
        self._db = mysql.connector.connect(
          host="localhost",
          user=dbUser,
          password=dbPassword
        )
        self._dbCursor = self._db.cursor()

    def addUser(self, slackUser : SlackUser, trelloUser: TrelloUser ):
        #TODO print log?
        #TODO raise exception based on how it goes
        
        sql = "INSERT INTO "+table_name+" (slackUserName, slackID, trelloUserName, trelloID) VALUES (%s, %s, %s, %s)"
        data = (slackUser.name, slackUser.id, trelloUser.username, trelloUser.id)
        self._dbCursor.execute(sql, data)
        self._db.commit()

    def removeUser(self, slackUser : SlackUser):
        print('remove user')
        #TODO remove a user
        #raise exception based on how it goes

    def getSlackUser(self, trelloUser: TrelloUser):
        #TODO print log?
        #TODO raise exception based on how it goes
        
        sql = "SELECT * FROM "+table_name+" WHERE trelloID = %s"
        data = (trelloUser.id,)
        self._dbCursor.execute(sql, data)
        result = self._dbCursor.fetchall()
        
        #TODO deal with result
        return self._slack.getSlackUserByID()

    def getTrelloUser(self, slackUser : SlackUser):
        #TODO print log?
        #TODO raise exception based on how it goes
        
        sql = "SELECT * FROM "+table_name+" WHERE slackID = %s"
        data = (slackUser.id, )
        self._dbCursor.execute(sql, data)
        result = self._dbCursor.fetchall()
        
        #TODO deal with result
        return self._trello.getUserByID()
