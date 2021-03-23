from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

class AnswerFAQPlugin(MachineBasePlugin):

    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=r'{self.settings['COMMAND_TOKEN']}\s*nyckel') #TODO borde brytas ut till say istället för reply. Hur görs det snyggt?
    def keyQuestion(self, msg):
        msg.reply(":key: Du vill nog ha info om nyckelutlämningar. TBC :)", in_thread=True)
        
    @listen_to(regex=r'{self.settings['COMMAND_TOKEN']}\s*box')
    @listen_to(regex=r'{self.settings['COMMAND_TOKEN']}\s*låda')
    def boxQuestion(self, msg):
        msg.say(":key: Du vill nog ha info om lådor och förvarring. TBC :)", in_thread=True)
