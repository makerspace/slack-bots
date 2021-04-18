import os, re

#TODO move to settings file
commandChar = '!'
argChar = ':'

class Command:

    def __init__(self, command, description, numArg=None, aliases = None):
        self.command = command
        self.description = description
        self.numArg = numArg
        self.aliases = aliases
        
        if self.numArg == None:
            self.regex = Command.createRegEx(self.command, aliases)
        else:
            self.regex = Command.createRegExWithArgument(self.command, self.numArg, aliases)

    def __str__(self):
        if self.numArg == None:
            return commandChar+self.command+" "+self.description
        else:
            return commandChar+self.command+" tar "+str(self.numArg)+" argument. "+self.description

    def _createRegEx(command):
        return '^'+re.escape(commandChar)+'\s*'+re.escape(command)+'\s*$'

    def _createRegExWithArgument(command, numArg):
        return '^'+re.escape(commandChar)+'\s*'+re.escape(command)+'(\s*'+re.escape(argChar)+'\s*\w{1,}){'+re.escape(str(numArg))+'}\s*$'

    def createRegEx(command, aliases):
        regex_str = Command._createRegEx(command)
        if aliases != None:
            for a in aliases:
                regex_str += '|'+Command._createRegEx(a)
        return r''+regex_str
   
    def createRegExWithArgument(command, numArg, aliases):
        regex_str = Command._createRegExWithArgument(command, numArg)
        if aliases != None:
            for a in aliases:
                regex_str += '|'+Command._createRegExWithArgument(a, numArg)
        return r''+regex_str

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
