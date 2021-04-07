import os, re

#TODO move to settings file
commandChar = '!'
argChar = ':'

class Command:

    def __init__(self, command, description, numArg=None):
        self.command = command
        self.description = description
        self.numArg = numArg
        
        if self.numArg == None:
            self.regex = Command.createRegEx(self.command)
        else:
            self.regex = Command.createRegExWithArgument(self.command, self.numArg)

    def __str__(self):
        if self.numArg == None:
            return commandChar+self.command+" "+self.description
        else:
            return commandChar+self.command+" tar "+str(self.numArg)+" argument. "+self.description

    def createRegEx(word):
        return r'^'+re.escape(commandChar)+'\s*'+re.escape(word)+'\s*$'
   
    def createRegExWithArgument(word, numArg):
        return r'^'+re.escape(commandChar)+'\s*'+re.escape(word)+'(\s*'+re.escape(argChar)+'\s*\w{1,}){'+re.escape(str(numArg))+'}\s*$'

class CommandDescriptions:
    
    def __init__(self):
        self.commands = []

    def __str__(self):
        res = str(self.commands[0])
        for index in range(1,len(self.commands)):
            res += '\n'+str(self.commands[index])
        return res
    
    def add(self, command:Command):
        self.commands.append(command)
