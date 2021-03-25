from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

class AnswerFAQPlugin(MachineBasePlugin):
    commandToken = '!'

    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*about\s*$')
    def aboutQuestion(self, msg):
        msgToSend="Vi har lite olika slack bottar.\nFAQ bot: "+self.commandToken+"aboutfaq"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*aboutfaq\s*$')
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor.\n !nyckel !box !faq"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*faq\s*$')
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*nyckel$')
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*box\s*$')
    @listen_to(regex=r'^'+re.escape(commandToken)+'\s*låda\s*$')
    def boxQuestion(self, msg):
        msgToSend="Maximala måtten för labblåda är ca 50 x 39 x 26 cm. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Makerspace_FAQ#F%C3%B6rvaring"
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)
