import mysql.connector

#TODO move to settings file
database_name = 'slack_trello'
table_name = 'users'

dbUser = os.getenv('MYSQL_USER')
dbPassword = os.getenv('MYSQL_PASSWORD')
if dbUser == None:
    raise RuntimeError('MYSQL_USER not set')
if dbPassword == None:
    raise RuntimeError('MYSQL_PASSWORD not set') 

db = mysql.connector.connect(
  host="localhost",
  user=dbUser,
  password=dbPassword
)
dbCursor = db.cursor()

#TODO check if database exists
dbCursor.execute('CREATE DATABASE '+database_name)

dbCursor.execute('CREATE TABLE'+table_name+' (id INT AUTO_INCREMENT PRIMARY KEY, slackUserName VARCHAR(30), slackID VARCHAR(255), trelloUserName VARCHAR(30), trelloID VARCHAR(255))')
