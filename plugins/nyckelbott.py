from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

class AnswerKeyQuestionsPlugin(MachineBasePlugin):

    @listen_to(regex=r'nyckelutlämning.*\?')
    def question(self, msg):
        msg.reply(":key: Du vill nog ha info om nyckelutlämningar. TBC :)", in_thread=True)
