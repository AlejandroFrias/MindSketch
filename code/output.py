import sublime, sublime_plugin, re, string, collections


class PromptMindSketchCommand(sublime_plugin.WindowCommand):

	def run(self):
		self.window.show_input_panel("Insert Text:", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		try:
			line = text
			if self.window.active_view():
				self.window.active_view().run_command("mind_sketch", {"line": line} )
		except ValueError:
			pass

class MindSketchCommand(sublime_plugin.TextCommand):

	def run(self, edit, line):
		language = re.match("[a-z]+.([^ ]+).*", self.view.scope_name(self.view.sel()[0].begin())).group(1)
		print("language: " + language)

		# TODO
		(name, m) = parsers.match(line)

		# Exit out if the command didn't match anything
		if not(m):
			print("Command: '" + line + "' did not match any Translator Objects")
			insert_code(self, edit, line)
			return
		else:
			print("Matched to translator object: " + name)

		if code_snippets.has_snippet(name, language):
			code = code_snippets.get(name, language).format(m.groupdict())
			self.view.run_command("insert_snippet", { "contents": code })
		else:
			error = "No code snippet supplied for translator object: " + name + \
			" and language: " + language
			print(error)
			insert_code(self, edit, error + "\n" + "command: " + line)

		
def insert_code(self, edit, code):
	for region in self.view.sel():
			(row, column) = self.view.rowcol(region.begin())
			indent = self.view.substr(sublime.Region(self.view.line(region.begin()).begin(), region.begin()))
			self.view.replace(edit, region, reindent(code, indent))

# Indents all lines except the first to match the indentation level of the first line
def reindent(s, indent):
	s1 = s.split('\n')
	for i in range(1, len(s1)):
		s1[i] = indent + s1[i]
	return '\n'.join(s1)
		
def join(things):
	return "^" + " ?".join(things) +"$"

def gen_parser(things):
	regex = join(things)
	return re.compile(regex)

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
# The below code should be generated from user input file in my DSL.


# Translator Object: 'Basic class'
parsers.add('Basic class', (u'(generate|make|create)?', u'class', u'(?P<NAME>.*?)'))
parsers.add('Basic class', (u'(?P<NAME>.*?)', u'is', u'a', u'class'))
code_snippets.add('Basic class', 'java', """class ${{1:{0[NAME]}}} {{
	
}}""")

# Translator Object: 'Basic class'
code_snippets.add('Basic class', 'java', """class {0[NAME]} {{
	{0[NAME]}(${{1:args}}) {{
		$0
	}}
}}""")

# Translator Object: 'Basic for loop'
parsers.add('Basic for loop', (u'(generate|make)?', u'(for)?', u'loop', u'from', u'(?P<START>.*?)', u'to', u'(?P<END>.*?)'))
parsers.add('Basic for loop', (u'(lets)?', u'loop', u'(until|to)', u'(?P<END>.*?)', u'(starting at|from)', u'(?P<START>.*?)'))
code_snippets.add('Basic for loop', 'java', """for(int i = ${{1:{0[START]}}}; i < ${{2:{0[END]}}}; i++) {{
    $0
}}""")
code_snippets.add('Basic for loop', 'python', """for x in xrange(${{1:{0[START]}}}, ${{2:{0[END]}}}):
    ${{0:pass}}""")

# Translator Object: 'Print'
parsers.add('Print', (u'(print|say)', u'(?P<MESSAGE>.*?)', u'(to)?', u'(the)?', u'(console|screen)?'))
code_snippets.add('Print', 'java', """System.out.println(${{1:"{0[MESSAGE]}"}});
$0""")
code_snippets.add('Print', 'python', """print(${{1:"{0[MESSAGE]}"}})
$0""")

