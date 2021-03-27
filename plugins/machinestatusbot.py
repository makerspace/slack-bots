from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re, mysql.connector
import slackHelper as helper

class MachineStatusPlugin(MachineBasePlugin):

    @listen_to(regex=helper.createRegEx('aboutfaq'))
    def aboutMachineStatusQuestion(self, msg):
        msgToSend="Maskin status botten svarar på frågor om status på maskiner."
        helper.sendMessage(msg, msgToSend)

    @listen_to(regex=helper.createRegExWithArgument('setstatus',2))
    def setStatusSlack(self, msg):
        msgToSend="Sätt status på maskin"
        helper.sendMessage(msg, msgToSend)
        
    @listen_to(regex=helper.createRegExWithArgument('getstatus',1))
    def getStatusSlack(self, msg):
        msgToSend="Hämta maskin status, paj eller inte?"
        helper.sendMessage(msg, msgToSend)

#TODO addMachine
#TODO list broken machine all or for specific room
