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
def gen_parser(things):
	regex = "^" + " ?".join(things) +"$"
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
# The below code is generated from MindSketch file.


# Translator Object: Symbol(u'Basic class')
parsers.add(Symbol(u'Basic class'), (u'(generate|make|create)?', u'class', u'(?P<NAME>.*?)'))
parsers.add(Symbol(u'Basic class'), (u'(?P<NAME>.*?)', u'is', u'a', u'class'))
code_snippets.add(Symbol(u'Basic class'), 'java', """class ${{1:{0[NAME]}}} {{
	$0
}}""")
code_snippets.add(Symbol(u'Basic class'), 'python', """class ${{1:{0[NAME]}}}:
	$0""")

# Translator Object: Symbol(u'Basic reader')
parsers.add(Symbol(u'Basic reader'), (u'(generate|make|create)?', u'reader', u'(for)?', u'(?P<FILE>.*?)', u'named', u'(?P<NAME>.*?)'))
code_snippets.add(Symbol(u'Basic reader'), 'java', """BufferedReader ${{1:{0[NAME]}}} = new BufferedReader(new FileReader(${{2:{0[FILE]}}}));
$0""")

# Translator Object: Symbol(u'Basic for loop')
parsers.add(Symbol(u'Basic for loop'), (u'(generate|make)?', u'(for)?', u'loop', u'from', u'(?P<START>.*?)', u'to', u'(?P<END>.*?)'))
parsers.add(Symbol(u'Basic for loop'), (u'(lets)?', u'loop', u'(until|to)', u'(?P<END>.*?)', u'(starting at|from)', u'(?P<START>.*?)'))
code_snippets.add(Symbol(u'Basic for loop'), 'java', """for(int i = ${{1:{0[START]}}}; i < ${{2:{0[END]}}}; i++) {{
    $0
}}""")
code_snippets.add(Symbol(u'Basic for loop'), 'python', """for x in xrange(${{1:{0[START]}}}, ${{2:{0[END]}}}):
    ${{0:pass}}""")

# Translator Object: Symbol(u'Print')
parsers.add(Symbol(u'Print'), (u'(print|say)', u'(?P<MESSAGE>.*?)', u'(to)?', u'(the)?', u'(console|screen)?'))
code_snippets.add(Symbol(u'Print'), 'java', """System.out.println(${{1:"{0[MESSAGE]}"}});
$0""")
code_snippets.add(Symbol(u'Print'), 'python', """print(${{1:"{0[MESSAGE]}"}})
$0""")

