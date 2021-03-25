from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

class AnswerFAQPlugin(MachineBasePlugin):
    commandToken = '!'
   
    def createRegEx(word):
        commandToken = '!'
        return r'^'+re.escape(commandToken)+'\s*'+re.escape(word)+'\s*$'
        
    def sendMessage(self, msg, msgToSend):
        if msg.in_thread or not msg.text[0] == self.commandToken:
            msg.reply(msgToSend, in_thread=True)
        else:
            msg.say(msgToSend)

    @listen_to(regex=createRegEx('about'))
    def aboutQuestion(self, msg):
        msgToSend="Vi har lite olika slack bottar.\nFAQ bot: "+self.commandToken+"aboutfaq"
        self.sendMessage(msg, msgToSend)

    @listen_to(regex=createRegEx('aboutfaq'))
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor.\n !nyckel !box !faq"
        self.sendMessage(msg, msgToSend)

    @listen_to(regex=createRegEx('faq'))
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        self.sendMessage(msg, msgToSend)

    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=createRegEx('nyckel'))
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)"
        self.sendMessage(msg, msgToSend)

    @listen_to(regex=createRegEx('box'))
    @listen_to(regex=createRegEx('låda'))
    def boxQuestion(self, msg):
        msgToSend="Maximala måtten för labblåda är ca 50 x 39 x 26 cm. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Makerspace_FAQ#F%C3%B6rvaring"
        self.sendMessage(msg, msgToSend)
