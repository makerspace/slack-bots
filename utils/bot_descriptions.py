import os, re

#TODO move to settings file
commandChar = '!'
argChar = ':'

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Bot:

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __str__(self):
        return self.name+", "+self.desc

class BotDescriptions(metaclass=Singleton):
    general_usage = "Argument delas upp med " + argChar
    
    def __init__(self):
        self.bots = []
        print('asdf')

    def __str__(self):
        res = str(self.bots[0])
        for index in range(1,len(self.bots)):
            res += '\n'+str(self.bots[index])
        return self.general_usage + "\n" + res
    
    def add(self, bot:Bot):
        self.bots.append(bot)
