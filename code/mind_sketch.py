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

		p1 = re.compile(r"^generate for( loop)? from (?P<start>.*?) to (?P<end>.*?)( increment by (?P<amount>.*))?$")
		t1 ="""for (int i = {start}; i < {end}; i++) {{
    
}}"""

		parsers = [p1]
		templates = [t1]

		i = 0
		m = parsers[0].match(line)
		while not(m) and i < len(parsers) - 1:
			i += 1
			m = parsers[i].match(line)

		if not(m):
			print "Command: '" + line + "' did not match any Parser Objects"
			return
		# TODO, figure out a way to send format args better
		code = templates[i].format(start=m.group('start'), end=m.group('end'))

		for region in self.view.sel():
			(row, column) = self.view.rowcol(region.begin())
			self.view.insert(edit, region.begin(), reindent(code, column))

def reindent(s, numSpaces):
	s = string.split(s, '\n')
	for i in range(1, len(s)):
		s[i] = (numSpaces * ' ') + s[i]
	s = string.join(s, '\n')
	return s


