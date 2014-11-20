import sublime, sublime_plugin, re, string

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
		print "language: " + language

		# In order, try to match each regex from parsers to the input. Stop on first match
		i = 0

		m = gen_parser(parsers[0]).match(line)
		while not(m) and i < len(parsers) - 1:
			i += 1
			m = gen_parser(parsers[i]).match(line)

		# Exit out if the command didn't match anything
		# TODO: possible insert the error directly at cursor while also selecting it...
		if not(m):
			print "Command: '" + line + "' did not match any Parser Objects"
			insert_code(self, edit, line)
			return

		# Check to make sure there is code template supplied for the language of the file's language
		if not templates[i].has_key(language):
			error = "No code template supplied for language: " + language
			print error
			insert_code(self, edit, error + "\n" + "command: " + line)
			return

		# Create and insert the code snippet
		code = templates[i][language].format(m.groupdict())
		insert_code(self, edit, code)

		# Set the cursor to to right place by replacing $C
		if self.view.find("$C", 0, sublime.LITERAL):
			self.view.sel().clear()
		while self.view.find("$C", 0, sublime.LITERAL):
			next_region = self.view.find("$C", 0, sublime.LITERAL)
			self.view.replace(edit, next_region, "")
			self.view.sel().add(sublime.Region(next_region.begin(), next_region.begin()))

def insert_code(self, edit, code):
	for region in self.view.sel():
			(row, column) = self.view.rowcol(region.begin())
			indent = self.view.substr(sublime.Region(self.view.line(region.begin()).begin(), region.begin()))
			self.view.replace(edit, region, reindent(code, indent))

# Indents all lines except the first to match the indentation level of the first line
def reindent(s, indent):
	s = string.split(s, '\n')
	for i in range(1, len(s)):
		s[i] = indent + s[i]
	s = string.join(s, '\n')
	return s

def join(things):
	return "^" + " ?".join(things) +"$"

def gen_parser(tuple):
	regex = join(tuple)
	return re.compile(regex)


parsers = []
templates = []

# The below code should be generated from user input file in my DSL. Above is boiler plate (except for maybe the name)

parsers += [("(generate)?", "(for)?", "loop", "from", "(?P<start>.+?)", "to", "(?P<end>.+?)", "increment", "by", "(?P<amount>.+?)")]
templates += [{'java':"""for (int i = {0[start]}; i <= {0[end]}; i = i + {0[amount]}) {{
	$C
}}""", 'python':"""for x in xrange({0[start]}, {0[end]}, {0[amount]}):
	$C"""}]

parsers += [("(generate)?", "(for)?", "loop", "from", "(?P<start>.+?)", "to", "(?P<end>.+?)", "decrement", "by", "(?P<amount>.+?)")]
templates += [{'java':"""for (int i = {0[start]}; i <= {0[end]}; i = i + {0[amount]}) {{
	$C
}}""", 'python':"""for x in xrange({0[start]}, {0[end]}, {0[amount]}):
	$C"""}]

parsers += [("(generate)?", "(for)?", "loop", "from", "(?P<start>.+?)", "to", "(?P<end>.+?)")]
templates += [{'java':"""for (int i = {0[start]}; i <= {0[end]}; i++) {{
	$C
}}""", 'python':"""for x in xrange({0[start]}, {0[end]}):
	$C"""}]

parsers += [("(generate)?", "while", "(loop)?", "(?P<condition>.*?)")]
templates += [{'java':"""while ({0[condition]}) {{
	$C
}}""", 'python':"""while {0[condition]}:
	$C"""}]

parsers += [("(generate|create)?", "class", "(?P<name>.+?)", "(that)?", "extends", "(?P<parent>.+?)", "(and)?", "implements", "(?P<interface>.+?)")]
templates += [{'java':"""class {0[name]} extends {0[parent]} implements {0[interface]} {{
	$C
}}"""}]

parsers += [("(generate|create)?", "class", "(?P<name>.+?)", "(that)?", "extends", "(?P<parent>.+?)")]
templates += [{'java':"""class {0[name]} extends {0[parent]} {{
	$C
}}"""}]

parsers += [("(generate|create)?", "class", "(?P<name>.+?)", "(that)?", "implements", "(?P<interface>.+?)")]
templates += [{'java':"""class {0[name]} implements {0[interface]} {{
	$C
}}"""}]

parsers += [("(generate|create)?", "class", "(?P<name>.+?)")]
templates += [{'java':"""class {0[name]} {{
	$C
}}"""}]

parsers += [("(print|say)", "(?P<message>.+?)", "(to)?", "(the)?", "(console|screen)?")]
templates += [{'java':"""System.out.println("{0[message]}");
$C""", 
'python':"""print "{0[message]}"
$C"""}]

parsers += [("(generate|create)?", "main", "(method)?")]
templates += [{'java':"""public static void main(String[] args) {{
	$C
}}"""}]
