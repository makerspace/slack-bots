from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

class AnswerFAQPlugin(MachineBasePlugin):
    commandToken = '!'

    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*faq')
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*nyckel')
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*box')
    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*låda')
    def boxQuestion(self, msg):
        msgToSend="Maximala måtten för labblåda är ca 50 x 39 x 26 cm. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Makerspace_FAQ#F%C3%B6rvaring"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)
