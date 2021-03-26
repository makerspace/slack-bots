from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re
import slackHelper as helper

class AnswerFAQPlugin(MachineBasePlugin):
   
   #TODO use message payload for the weblinks?

    @listen_to(regex=helper.createRegEx('about'))
    def aboutBotsQuestion(self, msg):
        msgToSend="Vi har lite olika slack bottar.\nFAQ bot: "+helper.commandChar+"faqbot"
        helper.sendMessage(msg, msgToSend)

    @listen_to(regex=helper.createRegEx('!faqbot'))
    def aboutFAQQuestion(self, msg):
        msgToSend="Faq botten svarar på diverse frågor.\n !nyckel !box !faq" #TODO list commandas somehow?
        helper.sendMessage(msg, msgToSend)

    @listen_to(regex=helper.createRegEx('faq'))
    def faqQuestion(self, msg):
        msgToSend="Makerspace FAQ: https://wiki.makerspace.se/Makerspace_FAQ"
        helper.sendMessage(msg, msgToSend)

    @listen_to(regex=r'nyckelutlämning.*\?')
    @listen_to(regex=helper.createRegEx('nyckel'))
    def keyQuestion(self, msg):
        msgToSend=":key: Du vill nog ha info om nyckelutlämningar. TBC :)"
        helper.sendMessage(msg, msgToSend)

    @listen_to(regex=helper.createRegEx('box'))
    @listen_to(regex=helper.createRegEx('låda'))
    def boxQuestion(self, msg):
        msgToSend="Maximala måtten för labblåda är ca 50 x 39 x 26 cm. Mer info om förvaring på spacet och exempel på lådor finns på: https://wiki.makerspace.se/Makerspace_FAQ#F%C3%B6rvaring"
        helper.sendMessage(msg, msgToSend)
