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

comment = "#", { all characters }, newline;

name = { all characters - ":" }, ":";

group = "(", word, {"|", word }, ")", ["?"];
variable = "$", var letter, { [ "_" ], var letter };

regex = ( group | word | variable ), { space, ( group | word | variable ) };

parser object = { comment },
				"PARSER START", newline, 
				regex, newline, 
				"PARSER END";

language name = { ( letter | "." | "+" };
code snippet body = { all characters | "$C" | variable } (* just can't spell "CODE END" *)
code snippet = { comment }, 
				"CODE START:", space, language name, newline, 
				code snippet body, newline,
 				"CODE END"

translator = { comment }, name, { parser object }, { code snippet };

folder = { all characters - "/" };
relative_path = folder, { "/", folder }, ".misk";
imports = "import", white space, relative_path;

snake name = word, { "_", word };
command = "COMMAND:", space, snake name, newline,
          (group | word), { space, ( group | word ) }, newline,
          "COMMAND END" ;

grammar = { imports }, { command }, { translator };


@author  Alejandro Frias
@contact alejandro.frias@ymail.com
@version 2014.12.11
"""
from __future__ import unicode_literals, print_function
from pypeg2 import *
from pypeg2.xmlast import thing2xml
import os
import sys

# Includes words with numerals, capital letters and one apostrophe
lower_case_word = re.compile("[a-z']+") # re.compile("(?!PARSER END)(\w+'\w*|'\w+|\w+)")
upper_case_word = re.compile("[A-Z]+")
		
simple_group = re.compile("\([a-z']+( [a-z']+)*(\|[a-z']+( [a-z']+)*)*\)")
variable = re.compile("\$[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")

language = re.compile("[a-z\.\+]+")

code_snippet = re.compile("(?:(?!CODE END).+)(?:\n(?:(?!CODE END).*))*")

comment = re.compile("^#.*")

relative_path = re.compile("[^/\s]+(/[^/\s]+)*\.misk")

nav_command = re.compile("[a-z]+(_[a-z]+)*")

Symbol.regex = re.compile("[\s\w]+")

class Import(str):
	grammar = "import", relative_path, endl

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
			  "CODE START", ":", attr("language", LanguageName), contiguous(endl, \
			  code_snippet), endl,  \
			  "CODE END"

class Command(List):
	grammar = "COMMAND", ":", attr("command", nav_command), endl, \
			  some([Word, Group]), endl, \
			  "COMMAND END", endl

class TranslatorObject(List):
	grammar = attr("comments", maybe_some(Comment)), \
			  name(), ":", endl, \
			  attr("parser_objects", maybe_some(ParserObject)), endl, \
			  attr("code_snippets", maybe_some(CodeSnippet))

class MindSketch(List):
	grammar = attr("imports", maybe_some(Import)), attr("commands", maybe_some(Command)), maybe_some(TranslatorObject)

next

"""
Recursivley parse the file and any files it imports, preserving order as it appends 
all the translator objects and commands into one master MindSketch object.

It uses relative paths, cycle detection, and duplication detection.

@param misk_file A relative path to a misk_file to be parsed
@param directory A relative path of the directory of misk_file used to allow relative paths of imports
@return A single MindSketch object
"""
def recursive_parse(misk_file, current_directory=None, already_imported=None):
	
	# Artifact of python default parameters begin treated like static 
	# variables when they start as mutable
	if already_imported is None:
		already_imported = set()

	# This allows relative path names even in imports of imports.
	if current_directory is not None:
		print("Updating Current Directory to: " + current_directory)
		if os.path.abspath(os.path.join(misk_file, os.pardir)) != os.path.abspath(current_directory):
			misk_file = current_directory + "/" + misk_file

	# Prevents cycles and multiple imports
	if os.path.abspath(misk_file) in already_imported:
		print("Already Imported: " + misk_file)
		print("Prev Imports: " + repr(already_imported))
		return []

	print("Opening: " + misk_file)
	with open(misk_file, "r") as f:
		text = f.read() 

	print("Parsing: " + misk_file)
	ast = parse(text, MindSketch, misk_file)

	# Base case: no more imports
	if len(ast.imports) == 0:
		return ast

	already_imported.add(os.path.abspath(misk_file))
	parent_directory = os.path.abspath(os.path.join(misk_file, os.pardir))

	# Recursively parse all the imports
	imports = [recursive_parse(t, parent_directory, already_imported) for t in ast.imports]
	
	# Compose all imported navigation commands into one list
	nav_commands = []
	for im in imports:
		if type(im) == MindSketch:
			nav_commands += im.commands
	nav_commands.extend(ast.commands)

	# Compose all imported Translator Objects into one list
	tobjects = [tobject for misk in imports for tobject in misk]
	ast.extend(tobjects)

	new_ast = MindSketch(ast)
	new_ast.commands = nav_commands
	new_ast.imports = ast.imports

	return new_ast
