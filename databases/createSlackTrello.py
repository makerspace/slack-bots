import mysql.connector, os

#TODO move to settings file
database_name = 'slack_trello'
table_name = 'users'

dbUser = os.getenv('MYSQL_BOT_USER')
dbPassword = os.getenv('MYSQL_BOT_PASSWORD')
if dbUser == None:
    raise RuntimeError('MYSQL_BOT_USER not set')
if dbPassword == None:
    raise RuntimeError('MYSQL_BOT_PASSWORD not set') 

db = mysql.connector.connect(
  host="localhost",
  user=dbUser,
  password=dbPassword
)
dbCursor = db.cursor()

dbCursor.execute('CREATE DATABASE IF NOT EXISTS '+database_name)

dbCursor.execute('USE '+database_name)
dbCursor.execute('CREATE TABLE IF NOT EXISTS '+table_name+' (id INT AUTO_INCREMENT PRIMARY KEY, slackUserName VARCHAR(30), slackID VARCHAR(255), trelloUserName VARCHAR(30), trelloID VARCHAR(255))')
db.commit()
