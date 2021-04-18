import re, os, pytest
from utils.command_descriptions import Command, CommandDescriptions

test_str = 'test'
test_alias = 'alias'
test_alias2 = 'alias2'
commandChar = os.getenv('BOT_COMMAND_CHAR')
argChar = os.getenv('BOT_ARG_CHAR')

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str, True), ("not a command", False), (commandChar+" "+test_str+" ", True), (commandChar+test_str+" word", False), (commandChar+test_str+"word", False)])
def test_regexp(test_input, expected):
    command = Command(test_str, 'description')
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str, False), (commandChar+test_str+argChar+" ", False), (commandChar+test_str+argChar+"word", True), ("not a command", False), (commandChar+" "+test_str+argChar+" word", True), (commandChar+test_str+" word"+argChar, False), (commandChar+test_str+"word"+argChar, False)])
def test_regexp_arguments(test_input, expected):
    command = Command(test_str, 'description', 1)
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str+argChar+" "+argChar, False), (commandChar+test_str+argChar+"word"+argChar+"", False), (commandChar+test_str+argChar+"word"+argChar+"word", True), (commandChar+" "+test_str+argChar+" word", False), (commandChar+test_str+" word"+argChar, False)])
def test_regexp_arguments_multiple(test_input, expected):
    command = Command(test_str, 'description', 2)
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str, True), (commandChar+test_alias, True)])
def test_regexp_alias(test_input, expected):
    command = Command(test_str, 'description', aliases=[test_alias])
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str, False), (commandChar+test_alias, False), (commandChar+test_str+argChar+"word", True), (commandChar+test_alias+argChar+"word", True)])
def test_regexp_arguments_alias(test_input, expected):
    command = Command(test_str, 'description', 1, aliases=[test_alias])
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str, True), (commandChar+test_alias, True), (commandChar+test_alias2, True), (commandChar+test_str+argChar+"word", False), (commandChar+test_alias+argChar+"word", False), (commandChar+test_alias2+argChar+"word", False)])
def test_regexp_alias_multiple(test_input, expected):
    test_alias_mult = [test_alias, test_alias2]
    command = Command(test_str, 'description', aliases=test_alias_mult)
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex

@pytest.mark.parametrize("test_input,expected", [(commandChar+test_str, False), (commandChar+test_alias, False), (commandChar+test_alias2, False), (commandChar+test_str+argChar+"word", True), (commandChar+test_alias+argChar+"word", True), (commandChar+test_alias2+argChar+"word", True)])
def test_regexp_arguments_alias_multiple(test_input, expected):
    test_alias_mult = [test_alias, test_alias2]
    command = Command(test_str, 'description', 1, aliases=test_alias_mult)
    res = re.search(command.regex, test_input)
    assert (res != None) == expected, '\n'+test_input+'\n'+command.regex
