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
		print self.view.scope_name(self.view.sel()[0].begin())

		parsers = []
		templates = []

		parsers += [re.compile(r"^(generate )?for loop from (?P<start>.+?) to (?P<end>.+?) increment by (?P<amount>.+?)$")]
		templates += ["""for (int i = {0[start]}; i <= {0[end]}; i = i + {0[amount]}) {{
    $C
}}"""]

		parsers += [re.compile(r"^(generate )?for loop from (?P<start>.+?) to (?P<end>.+?) decrement by (?P<amount>.+?)$")]
		templates += ["""for (int i = {0[start]}; i <= {0[end]}; i = i - {0[amount]}) {{
    $C
}}"""]
		parsers += [re.compile(r"^(generate )?for loop from (?P<start>.+?) to (?P<end>.+?)$")]
		templates += ["""for (int i = {0[start]}; i <= {0[end]}; i++) {{
    $C
}}"""]

		parsers += [re.compile(r"^(generate )?while (loop )?(?P<condition>.+?)$")]
		templates += ["""while ({0[condition]}) {{
    $C
}}"""]

		parsers += [re.compile(r"^((generate|create) )?class (?P<name>.+?) (that )?extends (?P<parent>.+?) (and )?implements (?P<interface>.+?)$")]
		templates += ["""class {0[name]} extends {0[parent]} implements {0[interface]} {{
    $C
}}"""]

		parsers += [re.compile(r"^((generate|create) )?class (?P<name>.+?) (that )?extends (?P<parent>.+?) (and )?implements (?P<interface>.+?)$")]
		templates += ["""class {0[name]} extends {0[parent]} implements {0[interface]} {{
    $C
}}"""]

		parsers += [re.compile(r"^((generate|create) )?class (?P<name>.+?) (that )?extends (?P<parent>.+?)$")]
		templates += ["""class {0[name]} extends {0[parent]} {{
    $C
}}"""]

		parsers += [re.compile(r"^((generate|create) )?class (?P<name>.+?) (that )?implements (?P<interface>.+?)$")]
		templates += ["""class {0[name]}implements {0[interface]} {{
    $C
}}"""]

		parsers += [re.compile(r"^((generate|create) )?class (?P<name>.+?)$")]
		templates += ["""class {0[name]} {{
    $C
}}"""]

		parsers += [re.compile(r"^(print|say) (?P<message>.+?)( to (the )?(console|screen))?$")]
		templates += ["""System.out.println("{0[message]}");$C"""]

		# In order, try to match each regex from parsers to the input. Stop on first match
		i = 0
		m = parsers[0].match(line)
		while not(m) and i < len(parsers) - 1:
			i += 1
			m = parsers[i].match(line)

		if not(m):
			print "Command: '" + line + "' did not match any Parser Objects"
			return
		
		# Create and insert the code snippet
		code = templates[i].format(m.groupdict())
		for region in self.view.sel():
			(row, column) = self.view.rowcol(region.begin())
			self.view.insert(edit, region.begin(), reindent(code, column))

		# Set the cursor to to right place by replacing $C
		for region in self.view.find_all("$C", sublime.LITERAL):
			self.view.sel().clear()
			self.view.sel().add(region)
			self.view.replace(edit, region, "")

# Indents all lines except the first to match the indentation level of the first line
def reindent(s, numSpaces):
	s = string.split(s, '\n')
	for i in range(1, len(s)):
		s[i] = (numSpaces * ' ') + s[i]
	s = string.join(s, '\n')
	return s
