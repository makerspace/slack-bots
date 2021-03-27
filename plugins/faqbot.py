from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

from utils.slackUtil import SlackUtil
import utils.regexFunctions as rFunc

class AnswerFAQPlugin(MachineBasePlugin):
   
   #TODO use message payload for the weblinks?

    #def init(self):

    def init_final(self):
        self.slackUtil = SlackUtil(self)

    @listen_to(regex=rFunc.createRegEx('about'))
    def aboutBotsQuestion(self, msg):
        msgToSend="Vi har lite olika slack bottar.\nFAQ bot: "+helper.commandChar+"faqbot"
        self.slackUtil.sendMessage(msgToSend, msg)

    @listen_to(regex=rFunc.createRegEx('!faqbot'))
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor.\n !nyckel !box !faq" #TODO list commands somehow?
        self.slackUtil.sendMessage(msgToSend, msg)

    @listen_to(regex=rFunc.createRegEx('faq'))
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        self.slackUtil.sendMessage(msgToSend, msg)

    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=rFunc.createRegEx('nyckel'))
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)" #TODO
        self.slackUtil.sendMessage(msgToSend, msg)

    @listen_to(regex=rFunc.createRegEx('box'))
    @listen_to(regex=rFunc.createRegEx('låda'))
    def boxQuestion(self, msg):
        msgToSend="Maximala måtten för labblåda är ca 50 x 39 x 26 cm. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Makerspace_FAQ#F%C3%B6rvaring"
        self.slackUtil.sendMessage(msgToSend, msg)

#TODO wiki link
