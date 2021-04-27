import os, mysql.connector
from trello import Member as TrelloUser
from machine.models.user import User as SlackUser

from base.slack import Slack
from base.trello import Trello

class SlackTrelloDB():

    def __init__(self, slack:Slack, trello:Trello, database_name, table_name):
        self._slack = slack
        self._trello= trello
        self._database_name = database_name
        self._table_name = table_name

        dbUser = os.getenv('MYSQL_BOT_USER')
        dbPassword = os.getenv('MYSQL_BOT_PASSWORD')
        if dbUser == None:
            raise RuntimeError('MYSQL_BOT_USER not set')
        if dbPassword == None:
            raise RuntimeError('MYSQL_BOT_PASSWORD not set')

        self._db_config = {
            'host': "localhost",
            'user': dbUser,
            'password': dbPassword,
            'database': self._database_name
        }

    def _openDB(self):
        self._db = mysql.connector.connect(**self._db_config)
        self._dbCursor = self._db.cursor()

    def _closeDB(self):
        self._dbCursor.close()
        self._db.close()

    def addUser(self, slackUser : SlackUser, trelloUser: TrelloUser ):
        #TODO raise exception based on how it goes
        self._openDB()

        sql = "INSERT INTO "+self._table_name+" (slackUserName, slackID, trelloUserName, trelloID) VALUES (%s, %s, %s, %s)"
        data = (slackUser.name, slackUser.id, trelloUser.username, trelloUser.id)
        self._dbCursor.execute(sql, data)
        self._db.commit()
        self._closeDB()

    def removeUserBySlack(self, slackUser : SlackUser):
        #TODO raise exception based on how it goes
        self._openDB()
        sql = "DELETE FROM " + self._table_name + " WHERE slackID = %s"
        data = (slackUser.id,)
        self._dbCursor.execute(sql, data)
        self._db.commit()
        self._closeDB()

    def removeUserByTrello(self, trelloUser : TrelloUser):
        #TODO raise exception based on how it goes
        self._openDB()
        sql = "DELETE FROM " + self._table_name + " WHERE trelloID = %s"
        data = (trelloUser.id,)
        self._dbCursor.execute(sql, data)
        self._db.commit()
        self._closeDB()

    def getSlackUser(self, trelloUser: TrelloUser):
        self._openDB()
        sql = "SELECT * FROM "+self._table_name+" WHERE trelloID = %s"
        data = (trelloUser.id,)
        self._dbCursor.execute(sql, data)
        result = self._dbCursor.fetchall()
        self._closeDB()

        if len(result) == 0:
            raise ValueError("No trello user in DB with: "+trelloUser.id+ " "+trelloUser.username)
        if len(result) != 1:
            raise RuntimeError("Database error, multiple users with same ID.")
        slack_id = result[0][2]
        return self._slack.getUserByID(slack_id)

    def getTrelloUser(self, slackUser : SlackUser):
        self._openDB()
        sql = "SELECT * FROM "+self._table_name+" WHERE slackID = %s"
        data = (slackUser.id,)
        self._dbCursor.execute(sql, data)
        result = self._dbCursor.fetchall()
        self._closeDB()

        if len(result) == 0:
            raise ValueError("No slack user in DB with: "+slackUser.id+ " "+slackUser.name)
        if len(result) != 1:
            raise RuntimeError("Database error, multiple users with same ID.")
        trello_id = result[0][4]
        return self._trello.getUserByID(trello_id)
