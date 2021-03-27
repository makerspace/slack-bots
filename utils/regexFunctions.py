import re, os

commandChar = '!'
argChar = ':'

def createRegEx(word):
    return r'^'+re.escape(commandChar)+'\s*'+re.escape(word)+'\s*$'
        
def createRegExWithArgument(word, numArg):
    return r'^'+re.escape(commandChar)+'\s*'+re.escape(word)+'(\s*'+re.escape(argChar)+'\s*\w{1,}){'+re.escape(str(numArg))+'}\s*$'
