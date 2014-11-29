"""MindSketch parser

This file is a parser for the MindSketch language written using pypeg2

Grammar of MindSketch:

white space = ? white space characters ?;
all characters = ? all visible characters ?;
space = " ";
newline = ? newline character ?;
letter = ? lower case letters ?;
var letter = ? upper case letters ?;
word = { letter };

comment = "#", { all characters }, newline

name = { all characters - ":" }, ":";

group = "(", word, {"|", word }, ")", ["?"];
variable = "$", var letter, { [ "_" ], var letter }

regex = (group | word | variable ), { space, ( group | word - "PARSER END" | variable ) };

parser object = { comment }, "PARSER START", newline, regex, newline, "PARSER END";

language name = { ( letter | "." | "+" };
code snippet body = { all characters | "$C" | variable } (* just can't spell "CODE END" *)
code snippet = { comment }, "CODE START:", space, language name, newline, code snippet body, newline, "CODE END"

translator = { comment }, name, { parser object }, { code snippet };

grammar = { translator };


@author  Alejandro Frias
@contact alejandro.frias@ymail.com
@version 2014.11.26
"""
from __future__ import unicode_literals, print_function
from pypeg2 import *
from pypeg2.xmlast import thing2xml


lower_case_word = re.compile("[a-z]+")
upper_case_word = re.compile("[A-Z]+")
		
simple_group = re.compile("\([a-z]+( [a-z]+)*(\|[a-z]+( [a-z]+)*)*\)\??")
variable = re.compile("\$[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")

language = re.compile("[a-z\.\+]+")

code_snippet = re.compile("(?:(?!CODE END).)+(?:\n(?:(?!CODE END).)+)*")

comment = re.compile("^#.*")

Symbol.regex = re.compile("[\s\w]+")

class Comment(str):
	# Using contiguous to capture any whitespace after the '#'
	# So that user defined spacing is preserved
	grammar = contiguous("#", restline)

class Variable(str):
	grammar = variable

class Word(str):
	grammar = lower_case_word

class Group(str):
	grammar = simple_group

class ParserObject(List):
	grammar = attr("comments", maybe_some(Comment)), \
			  "PARSER START", endl, \
	          some([Word, Variable, Group]), endl, \
	          "PARSER END", endl

class LanguageName(str):
	grammar = language

class CodeSnippet(str):
	grammar = attr("comments", maybe_some(Comment)), \
			  "CODE START", ":", attr("language", LanguageName), endl, \
			  code_snippet, endl,  \
			  "CODE END"

class TranslatorObject(List):
	grammar = attr("comments", maybe_some(Comment)), \
			  name(), ":", endl, \
			  attr("parser_objects", maybe_some(ParserObject)), endl, \
			  attr("code_snippets", maybe_some(CodeSnippet))

class MindSketch(List):
	grammar = some(TranslatorObject)
