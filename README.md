# Makerspace slack bots

Slack bots used at Stockholm Makerspace

## Usage

Requires various environmental variables to be used for the SQL, Slack and Trello. You need to set:
TRELLO_API_KEY, TRELLO_API_SECRET=, TRELLO_TOKEN_KEY, TRELLO_TOKEN_SECRET, MYSQL_BOT_USER, MYSQL_BOT_PASSWORD, BOT_COMMAND_CHAR, BOT_ARG_CHAR, SM_SLACK_API_TOKEN, BOT_CALENDAR_URL

You also proably want to change things in local_settings.py.

### Dependencies

py-test
py-trello
Currently requries a fork of slack-machine found here: https://github.com/makerspace/slack-machine
