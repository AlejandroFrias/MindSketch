from __future__ import unicode_literals, print_function
from pypeg2 import *
from pypeg2.xmlast import thing2xml

lower_case_word = re.compile("[a-z]+")
upper_case_word = re.compile("[A-Z]+")

simple_group = re.compile("\([a-z]+(\|[a-z]+)*\)\??")

variable = re.compile("\$[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")

language = re.compile("[a-z\.\+]+")

code_snippet = re.compile("(?:(?!CODE END).)+(?:\n(?:(?!CODE END).)+)*")

Symbol.regex = re.compile("[\s\w]+")

class Variable(str):
	grammar = variable

class Word(str):
	grammar = lower_case_word

class Group(str):
	grammar = simple_group
	

class ParserDefine(List):
	grammar = "PARSER START", endl, \
	          some([Word, Variable, Group]), endl, \
	          "PARSER END", endl

class Language(str):
	grammar = language

class CodeSnippet(str):
	grammar = "CODE START", ":", attr("language", Language), endl, \
			  code_snippet, endl,  \
			  "CODE END"

class TranslatorObject(List):
	grammar = name(), ":", endl, \
			  attr("parser", ParserDefine), endl, \
			  some(CodeSnippet)

class MindSketch(List):
	grammar = some(TranslatorObject)

def test():
	s = """PARSER START
	some (words)? (to|too) parse $VAR and $VAR_2
	PARSER END"""

	f = parse(s, ParserDefine)
	print(thing2xml(f, pretty=True).decode())

	s1 = """CODE START: java
while (${1:$CONDITION}) {
	$0
}
CODE END"""
	f1 = parse(s1, CodeSnippet)
	print(thing2xml(f1, pretty=True).decode())

	s2 = """
Title of translator object:

PARSER START
some (words)? (to|too) parse $CONDITION
PARSER END

CODE START: java
while (${1:$CONDITION}) {
	$0
}
CODE END

CODE START: python
while ${1:$CONDITION}:
	${0:pass}
CODE END
"""
	f2 = parse(s2, MindSketch)
	print(thing2xml(f2, pretty=True).decode())
	print(f2)
	print(f2[0].name)
	print(f2[0].parser)
	print(f2[0][1].language)

if __name__ == '__main__':
	test()
