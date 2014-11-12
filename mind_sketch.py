import sublime, sublime_plugin

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

		for region in self.view.sel():
			self.view.insert(edit, region.begin(), line)

