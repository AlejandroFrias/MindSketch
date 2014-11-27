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
		# TODO: think about creating the format_snippet method that doubles up on curley braces 
		#       and translates variables from $VAR to {0[VAR]}
		# code_snippet = format_snippet(code_snippet)
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

# Above is boiler plate (except for maybe the name)
# The below code should be generated from user input file in my DSL.


parsers.add("For loop with increment", ("(generate)?", "(for)?", "loop", "from", "(?P<start>.+?)", "to", "(?P<end>.+?)", "increment", "by", "(?P<amount>.+?)"))
code_snippets.add("For loop with increment", "java", """for (int i = {0[start]}; i <= {0[end]}; i = i + {0[amount]}) {{
	$0
}}""")
code_snippets.add("For loop with increment", "python", """for x in xrange({0[start]}, {0[end]}, {0[amount]})
	$0""")

parsers.add("For loop with decrement", ("(generate)?", "(for)?", "loop", "from", "(?P<start>.+?)", "to", "(?P<end>.+?)", "decrement", "by", "(?P<amount>.+?)"))
code_snippets.add("For loop with decrement", "java", """for (int i = {0[start]}; i <= {0[end]}; i = i - {0[amount]}) {{
	$0
}}""")
code_snippets.add("For loop with decrement", "python", """for x in xrange({0[start]}, {0[end]}, -{0[amount]})
	$0""")

parsers.add("Basic for loop", ("(generate)?", "(for)?", "loop", "from", "(?P<start>.+?)", "to", "(?P<end>.+?)"))
code_snippets.add("Basic for loop", "java", """for (int i = {0[start]}; i <= {0[end]}; i++) {{
	$0
}}""")
code_snippets.add("Basic for loop", "python", """for x in xrange({0[start]}, {0[end]}):
	$0""")

parsers.add("Basic while loop", ("(generate)?", "while", "(loop)?", "(?P<condition>.*?)"))
code_snippets.add("Basic while loop", "java", """while (${{1:{0[condition]}}}) {{
	$0
}}""")
code_snippets.add("Basic while loop", "python", """while ${{1:{0[condition]}}}:
	${{0:pass}}""")

parsers.add("Print", ("(print|say)", "(?P<message>.+?)", "(to)?", "(the)?", "(console|screen)?"))
code_snippets.add("Print", "java", """System.out.println("${{1:{0[message]}}}");
$0""")
code_snippets.add("Print", "python", """print(${{"1:{0[message]}"}})
$0""")

parsers.add("main method", ("(generate|create)?", "main", "(method)?"))
code_snippets.add("main method", "java", """public static void main(String[] args) {{
	$0
}}""")


