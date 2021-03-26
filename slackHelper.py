import re, os

commandChar = '!'
argChar = ':'
        
def createRegEx(word):
    return r'^'+re.escape(commandChar)+'\s*'+re.escape(word)+'\s*$'
    
def createRegExWithArgument(word, numArg):
    return r'^'+re.escape(commandChar)+'\s*'+re.escape(word)+'(\s*'+re.escape(argChar)+'\s*\w{1,}){'+re.escape(str(numArg))+'}\s*$'

def sendMessage(msg, msgToSend):
    if msg.in_thread or not msg.text[0] == commandChar:
        msg.reply(msgToSend, in_thread=True)
    else:
        msg.say(msgToSend)

def sendStatusMessage(msg, msgToSend): #TODO change so it is always sent to a log channel as well
    if msg.in_thread or not msg.text[0] == commandChar:
        msg.reply(msgToSend, in_thread=True)
    else:
        msg.say(msgToSend)

def getArguments(msg):
    args = msg.text.split(argChar)[1:]
    [item.strip() for item in args]
    return args
