import re, os, pytest, mysql.connector
from pytest_mock import mocker

from databases.slack_trello_database import SlackTrelloDB
from tests.mocks.slack_user import SlackUserMock
from tests.mocks.trello_user import TrelloUserMock
from tests.mocks.slack import SlackMock
from tests.mocks.trello import TrelloMock

class TestSlackTrelloDB:

    #Assumes that the datbase db_name exists or the bot user has permission to create it
    db_name = "slack_trello_testdb"
    table_name = "test_table"

    def _openDB(self):
        self._db = mysql.connector.connect(**self._db_config)
        self._dbCursor = self._db.cursor()

    def _closeDB(self):
        self._dbCursor.close()
        self._db.close()

    def check_users(self, slack_users, trello_users):
        self._openDB()
        sql = "SELECT * FROM " + self.table_name
        self._dbCursor.execute(sql)
        result = self._dbCursor.fetchall()
        self._closeDB()

        if len(slack_users) != len(trello_users):
            assert False, "number of users missmatch "+str(len(slack_users)) + ","+str(len(trello_users))

        if len(result) != len(slack_users):
            assert False, " numbers of users("+str(len(slack_users))+") does not match with number of users in database("+str(len(result))+")"

        for i in range(len(result)):
            assert result[i][1] == str(slack_users[i].name)
            assert result[i][2] == str(slack_users[i].id)
            assert result[i][3] == str(trello_users[i].username)
            assert result[i][4] == str(trello_users[i].id)

    @pytest.fixture()
    def setup_teardown(self):
        #Get the SQL user information and set the config
        dbUser = os.getenv('MYSQL_BOT_USER')
        dbPassword = os.getenv('MYSQL_BOT_PASSWORD')
        if dbUser == None:
            raise RuntimeError('MYSQL_BOT_USER not set')
        if dbPassword == None:
            raise RuntimeError('MYSQL_BOT_PASSWORD not set') 

        self._db_config = {
            "host": "localhost",
            "user": dbUser,
            "password": dbPassword,
            "database": self.db_name
        }
    
        #Setup
        self._openDB()
        self._dbCursor.execute("DROP TABLE IF EXISTS "+self.table_name)
        self._db.commit()
        self._dbCursor.execute("CREATE DATABASE IF NOT EXISTS "+self.db_name)
        self._dbCursor.execute("CREATE TABLE "+self.table_name+" (id INT AUTO_INCREMENT PRIMARY KEY, slackUserName VARCHAR(30), slackID VARCHAR(255), trelloUserName VARCHAR(30), trelloID VARCHAR(255))")
        self._db.commit()
        self._closeDB()

        yield self._db

        #Teardown
        self._openDB()
        self._dbCursor.execute('DROP TABLE '+self.table_name)
        self._db.commit()
        self._closeDB()

    @pytest.fixture
    def init(self, request):
        slack_trello = SlackTrelloDB(SlackMock(), TrelloMock(), self.db_name, self.table_name)
        slack_users = []
        trello_users = []
        for i in range(request.param):
            slack_user = SlackUserMock(str(i)+" Slack", 's'+str(i))
            trello_user = TrelloUserMock(str(i)+" Trello", 't'+str(i))
            slack_users.append(slack_user)
            trello_users.append(trello_user)
            slack_trello.addUser(slack_user, trello_user)
        return slack_trello, slack_users, trello_users

    @pytest.mark.parametrize("init", [1,5], indirect=["init"])
    def test_add_user(self, setup_teardown, init):
        slack_trello_DB, slack_users, trello_users = init
        self.check_users(slack_users, trello_users)
        
        slack_user = SlackUserMock("A Slack", 1)
        trello_user = TrelloUserMock("B Trello", 2)
        slack_users.append(slack_user)
        trello_users.append(trello_user)
        slack_trello_DB.addUser(slack_user,trello_user)
        self.check_users(slack_users, trello_users)

    @pytest.mark.parametrize("init", [5], indirect=["init"])
    def test_remove_user_slack(self, setup_teardown, init):
        slack_trello_DB, slack_users, trello_users = init
        self.check_users(slack_users, trello_users)

        index = 1
        slack_trello_DB.removeUserBySlack(slack_users[index])
        slack_users.remove(slack_users[index])
        trello_users.remove(trello_users[index])
        self.check_users(slack_users, trello_users)

        for i in range(len(slack_users)):
            slack_trello_DB.removeUserBySlack(slack_users[i])
        self.check_users([], [])

    @pytest.mark.parametrize("init", [5], indirect=["init"])
    def test_remove_user_trello(self, setup_teardown, init):
        slack_trello_DB, slack_users, trello_users = init
        self.check_users(slack_users, trello_users)

        index = 1
        slack_trello_DB.removeUserByTrello(trello_users[index])
        slack_users.remove(slack_users[index])
        trello_users.remove(trello_users[index])
        self.check_users(slack_users, trello_users)

        for i in range(len(slack_users)):
            slack_trello_DB.removeUserByTrello(trello_users[i])
        self.check_users([], [])

    @pytest.mark.parametrize("init", [5], indirect=["init"])
    def test_get_slack_user(self, setup_teardown, init):
        slack_trello_DB, slack_users, trello_users = init
        self.check_users(slack_users, trello_users)

        for i in range(len(slack_users)):
            assert slack_trello_DB.getSlackUser(trello_users[i]) == slack_users[i].id

        with pytest.raises(ValueError):
            slack_trello_DB.getSlackUser(TrelloUserMock('fake','fake'))

        self.check_users(slack_users, trello_users)

    @pytest.mark.parametrize("init", [5], indirect=["init"])
    def test_get_trello_user(self, setup_teardown, init):
        slack_trello_DB, slack_users, trello_users = init
        self.check_users(slack_users, trello_users)

        for i in range(len(slack_users)):
            assert slack_trello_DB.getTrelloUser(slack_users[i]) == trello_users[i].id

        with pytest.raises(ValueError):
            slack_trello_DB.getTrelloUser(SlackUserMock('fake','fake'))

        self.check_users(slack_users, trello_users)
