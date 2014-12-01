"""Generated from MindSketch

Suggested Key Binding:
	{ "keys": ["super+shift+m"], "command": "prompt_mind_sketch" }

@author  Alejandro Frias
@contact alejandro.frias@ymail.com
@version 2014.11.26
"""
import sublime, sublime_plugin, re, string, collections

# command = prompt_mind_sketch
# This command opens an input panel at the bottom of the screen
# for the english command to be inserted
class PromptMindSketchCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel("Insert Text:", "", self.on_done, None, None)

	def on_done(self, text):
		try:
			command = text
			if self.window.active_view():
				self.window.active_view().run_command("mind_sketch", {"command": command} )
		except ValueError:
			pass

# command = mind_sketch
# Attempts to parse and run the given command
class MindSketchCommand(sublime_plugin.TextCommand):

	def run(self, edit, command):
		# Gets the language of the file
		language = re.match("[a-z]+\.([^ ]+).*", self.view.scope_name(self.view.sel()[0].begin())).group(1)
		print("language: " + language)

		# Attempt to match the command to one of the parsers,
		# getting the name of the Translator Object in the process
		# as well as the Match object
		(name, m) = parsers.match(command)

		# Exit out if the command didn't match anything
		if not(m):
			print("Command: '" + command + "' did not match any Translator Objects")
			insert_code(self, edit, command)
			return
		else:
			print("Matched to translator object: " + name)

		# If there is a code snippet for Translator Object that matched
		# the command, then insert it with the variables gotten from the command
		# Otherwise print an error and insert an error for visibilit
		if code_snippets.has_snippet(name, language):
			code = code_snippets.get(name, language).format(m.groupdict())
			self.view.run_command("insert_snippet", { "contents": code })
		else:
			error = "No code snippet supplied for translator object: " + name + \
			" and language: " + language
			print(error)
			insert_code(self, edit, error + "\n" + "command: " + command)

# Helper method that inserts code at the cursor and selects it
def insert_code(self, edit, code):
	for region in self.view.sel():
			(row, column) = self.view.rowcol(region.begin())
			indent = self.view.substr(sublime.Region(self.view.line(region.begin()).begin(), region.begin()))
			self.view.replace(edit, region, reindent(code, indent))

# Indents all lines except the first to match the given indentation 
# level (ideally of the first line)
def reindent(s, indent):
	s1 = s.split('\n')
	for i in range(1, len(s1)):
		s1[i] = indent + s1[i]
	return '\n'.join(s1)

# The Parser Objects capture variables as non-greedy catch-all (".*?").
# In order to actually work, the whole command has to match, hence 
# the "^" and "$" that match the start and end of line respectively.
# Optional spaces bettwen the Parser Object's pieces allows for the optional
# groups to not add spaces.
# TODO: be smarter about spaces. optional means that words within words (like "is" inside of "otherwise" get caught too)
#       without it we don't get optional groups. for now not using optional groups...
def gen_parser(things):
	regex = "^" + " ".join(things) +"$"
	return re.compile(regex)

# A handy container for all the parser objects.
# Essentially an ordered dictionary of Translator Object name to Parser Object
# Ordered is important for how matching occurs. The first parser to 
# match wins!
class ParserContainer(object):
	def __init__(self):
		self.parser_dict = collections.OrderedDict()
	def add(self, name, parser_tuple):
		if name in self.parser_dict:
			self.parser_dict[name] += [gen_parser(parser_tuple)]
		else:
			self.parser_dict[name] = [gen_parser(parser_tuple)]
	def match(self, line):
		for name in self.parser_dict.keys():
			for parser in self.parser_dict[name]:
				if parser.match(line):
					return (name, parser.match(line))
		return (False, False)

# A handy container for all the code snippets.
# Essentially a dictionary of Translator Object names to their corresponding 
# code snippets.
# The groups of code snippets themselves is another dictionary from 
# language name to code snippet. This means only one code snippet per language
# per Translator Object.
# Added bonus feature: allows later overriding of snippets if you are
# copy-pasting or importing (TODO future feater) other people's Translator Objects
class CodeSnippetContainer(object):
	def __init__(self):
		self.code_snippet_dict = {}
	def add(self, name, language, code_snippet):
		if name in self.code_snippet_dict:
			self.code_snippet_dict[name][language] = code_snippet
		else:
			self.code_snippet_dict[name] = {language: code_snippet}
	def get(self, name, language):
		return self.code_snippet_dict[name][language]
	def has_snippet(self, name, language):
		result = True
		if name not in self.code_snippet_dict:
			result =  False
		elif language not in self.code_snippet_dict[name]:
			result = False
		return result



parsers = ParserContainer()
code_snippets = CodeSnippetContainer()

# Above is boiler plate
# The below code is generated from MindSketch file: examples/example.misk

# Translator Object: Plus

parsers.add('Plus', (u'plus',))
code_snippets.add('Plus', 'python', """+ $0""")

# Translator Object: Minus

parsers.add('Minus', (u'minus',))
code_snippets.add('Minus', 'python', """- $0""")

# Translator Object: String

parsers.add('String', (u'string', u'(?P<STRING>.*?)',))
code_snippets.add('String', 'python', """"{0[STRING]}"$0""")

# Translator Object: Basic Runnable Program

parsers.add('Basic Runnable Program', (u'(make|write)', u'a', u'(?P<NAME>.*?)', u'program',))
parsers.add('Basic Runnable Program', (u'(begin|build|make|write|create)', u'(?P<NAME>.*?)', u'program',))
parsers.add('Basic Runnable Program', (u'(make|write|build)', u'a', u'program', u'called', u'(?P<NAME>.*?)',))
code_snippets.add('Basic Runnable Program', 'python', """import sys

def {0[NAME]}():
	${{1:pass}}
$0

if __name__ == '__main__':
	{0[NAME]}()""")
code_snippets.add('Basic Runnable Program', 'java', """class {0[NAME]} {{
	public static void main(String[] args) {{
		$1
	}}
	$0
}}""")

# Translator Object: Basic class

parsers.add('Basic class', (u'(generate|make|create)', u'class', u'(?P<NAME>.*?)',))
parsers.add('Basic class', (u'(?P<NAME>.*?)', u'is', u'a', u'class',))
# Even the the Code Snippets can get
code_snippets.add('Basic class', 'java', """class ${{1:{0[NAME]}}} {{
	$2
}}
$3""")
# THeir own comments
code_snippets.add('Basic class', 'python', """class ${{1:{0[NAME]}}}:
	${{2:pass}}
$0""")

# Translator Object: Basic reader

parsers.add('Basic reader', (u'reader', u'for', u'(?P<FILE>.*?)', u'named', u'(?P<NAME>.*?)',))
code_snippets.add('Basic reader', 'java', """BufferedReader ${{1:{0[NAME]}}} = new BufferedReader(new FileReader(${{2:{0[FILE]}}}));
$0""")

# Translator Object: Basic for loop

parsers.add('Basic for loop', (u'loop', u'from', u'(?P<START>.*?)', u'to', u'(?P<END>.*?)',))
parsers.add('Basic for loop', (u'loop', u'(until|to)', u'(?P<END>.*?)', u'(starting at|from)', u'(?P<START>.*?)',))
code_snippets.add('Basic for loop', 'java', """for(int i = ${{1:{0[START]}}}; i < ${{2:{0[END]}}}; i++) {{
    $3
}}
$0""")
code_snippets.add('Basic for loop', 'python', """for x in xrange(${{1:{0[START]}}}, ${{2:{0[END]}}}):
    ${{3:pass}}
$0""")

# Translator Object: Print

parsers.add('Print', (u'(print|say)', u'(?P<MESSAGE>.*?)',))
code_snippets.add('Print', 'java', """System.out.println(${{1:"{0[MESSAGE]}"}});
$0""")
code_snippets.add('Print', 'python', """print(${{1:"{0[MESSAGE]}"}})
$0""")

# Translator Object: System arguments

parsers.add('System arguments', (u'(system argument|system arg|arg|argument)', u'number', u'(?P<POS>.*?)',))
parsers.add('System arguments', (u'get', u'the', u'(?P<POS>.*?)', u'(system argument|arg|argument)',))
code_snippets.add('System arguments', 'python', """sys.argv[${{1:{0[POS]}}}]$0""")

# Translator Object: Function Define

parsers.add('Function Define', (u'(define|create)', u'function', u'(?P<FUN>.*?)',))
parsers.add('Function Define', (u'function', u'(?P<FUN>.*?)',))
code_snippets.add('Function Define', 'python', """def {0[FUN]}($1):
	${{2:pass}}
$0""")

# Translator Object: Function Call

parsers.add('Function Call', (u'call', u'(?P<FUNCTION>.*?)', u'(with|on)', u'(?P<VARS>.*?)',))
code_snippets.add('Function Call', 'java', """{0[FUNCTION]}(${{1:{0[VARS]}}})$0""")
code_snippets.add('Function Call', 'python', """{0[FUNCTION]}(${{1:{0[VARS]}}})$0""")

# Translator Object: If else

parsers.add('If else', (u'if', u'(?P<CONDITION>.*?)', u'do', u'(?P<ACTION1>.*?)', u'(else|otherwise)', u'do', u'(?P<ACTION2>.*?)',))
parsers.add('If else', (u'do', u'(?P<ACTION1>.*?)', u'if', u'(?P<CONDITION>.*?)', u'otherwise', u'do', u'(?P<ACTION2>.*?)',))
code_snippets.add('If else', 'python', """if ${{1:{0[CONDITION]}}}:
	${{2:{0[ACTION1]}}}
else:
	${{3:{0[ACTION2]}}}
$0""")
code_snippets.add('If else', 'java', """if (${{1:{0[CONDITION]}}}) {{
	${{2:{0[ACTION1]}}}
}} else {{
	${{3:{0[ACTION2]}}}
}}
$0""")

# Translator Object: If Condition

parsers.add('If Condition', (u'if', u'(?P<CONDITION>.*?)', u'do', u'(?P<ACTION>.*?)',))
parsers.add('If Condition', (u'do', u'(?P<ACTION>.*?)', u'if', u'(?P<CONDITION>.*?)',))
code_snippets.add('If Condition', 'python', """if ${{1:{0[CONDITION]}}}:
	${{2:{0[ACTION]}}}
$0""")
code_snippets.add('If Condition', 'java', """if (${{1:{0[CONDITION]}}}) {{
	${{2:{0[ACTION]}}}
}}
$0""")

# Translator Object: Return

parsers.add('Return', (u'return', u'(?P<THING>.*?)',))
code_snippets.add('Return', 'python', """return ${{1:{0[THING]}}}
$0""")
code_snippets.add('Return', 'java', """return ${{1:{0[THING]}}};
$0""")

# Translator Object: Less than

parsers.add('Less than', (u'(?P<FIRST_THING>.*?)', u'(is less than|less than)', u'(?P<SECOND_THING>.*?)',))
code_snippets.add('Less than', 'python', """${{1:{0[FIRST_THING]}}} < ${{2:{0[SECOND_THING]}}}$0""")
code_snippets.add('Less than', 'java', """${{1:{0[FIRST_THING]}}} < ${{2:{0[SECOND_THING]}}}$0""")

# Translator Object: Greater than

parsers.add('Greater than', (u'(?P<FIRST_THING>.*?)', u'(is greater than|greater than)', u'(?P<SECOND_THING>.*?)',))
code_snippets.add('Greater than', 'python', """${{1:{0[FIRST_THING]}}} > ${{2:{0[SECOND_THING]}}}$0""")
code_snippets.add('Greater than', 'java', """${{1:{0[FIRST_THING]}}} > ${{2:{0[SECOND_THING]}}}$0""")

# Translator Object: Variable assignment

parsers.add('Variable assignment', (u'(?P<NAME>.*?)', u'(equals|is)', u'(?P<VALUE>.*?)',))
code_snippets.add('Variable assignment', 'python', """{0[NAME]} = ${{1:{0[VALUE]}}}
$0""")
code_snippets.add('Variable assignment', 'java', """{0[NAME]} = ${{1:{0[VALUE]}}};
$0""")

