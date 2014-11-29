"""Create Sublime Text 3 plugin from MindSketch

For help on usage: python create_plugin.py -h

Convert a MindSketch (.misk) file into a Sublime Text 3 plugin.
Does not work for Sublime Text 2 (without changing the python environment it uses to python3)

Save the resulting file into your Packages/Users folder and add
a binding for "prompt_mind_sketch".

Instructions to create the plugin:
1. Write a .misk file. For the example, calling it file.misk
2. In Terminal type: 'python create_plugin.py file.misk mind_sketch.py'
3. This created a plugin called 'mind_sketch.py'. Any name is fine as 
   long as the extension is '.py'. Save the plugin into Packages/User folder

Instructions for saving plugin to Sublime Text 3:
1. Get to Packages folder in menu 'Sublime Text -> Preferences -> Browse Packages'
2. Find 'User' folder
3. Save/drag the plugin there. (you may need to open up the file and save it to load the plugin)

Instructions for creating key binding in Sublime Text 3:
1. Open up 'Key Bindings - Users' located in menu 'Sublime Text -> Preferences -> Key Bindings - User'
2. Add '{ "keys": ["super+shift+m"], "command": "prompt_mind_sketch" }'
3. Modify "super+shift+m" to be whatever key binding you prefer

@author  Alejandro Frias
@contact alejandro.frias@ymail.com
@version 2014.11.26
"""
import argparse, mindsketch_parser, re, warnings, collections
from pypeg2 import parse

def main():
	p = argparse.ArgumentParser (description="Converts MindSketch (.misk) file into a Sublime Text 3.")
	p.add_argument("file", help=".misk file of Translator Objects")
	p.add_argument("output", help="file name to write to (inlude the file extension .py)")
	args = p.parse_args()

	print("Opening MindSketch file: " + args.file)
	text = "COULD NOT OPEN FILE"
	try:
		f = open(args.file, "r")
		text = f.read() 
		f.close
	except Exception, e:
		raise e

	# Parse the MindSketch file into an AST
	# Any Syntax errors will happen here
	print("Parsing: " + args.file)
	ast = parse(text, mindsketch_parser.MindSketch, args.file)

	translator_objects = TranslatorObjectList(ast)
	translator_objects.validate()

	output_lines = ["# The below code is generated from MindSketch file: " + args.file + "\n\n"]
	output_lines.extend(translator_objects.output_lines())

	# The bulk of the plugin work is boiler plate.
	print("Getting Boiler Plate plugin code")
	with open("source/code/plugin_template.py") as f:
		output_lines.insert(0, f.read())

	# Create the plugin
	print("Creating Plugin: " + args.output)
	with open(args.output, 'w') as f:
		f.writelines(output_lines)


"""
TranslatorObjectList organizes all the parsed translator objects for
easy validations and organized output to the plugin file
"""
class TranslatorObjectList(collections.OrderedDict):

	def __init__(self, translator_objects):
		super(TranslatorObjectList, self).__init__()
		for translator_object in translator_objects:
			self.add(translator_object)
		

	"""
	Adds a mindsketch_parser.TranslatorObject object to the list,
	merging it with any others with the same name.
	"""
	def add(self, translator_object):
		name = translator_object.name
		if name in self:
			self[name]["comments"] += translator_object.comments
		else:
			self[name] = {"comments": translator_object.comments, "parser_objects": [], "code_snippets": dict(), "variables": None}

		for parser_object in translator_object.parser_objects:
			self.add_parser_object(translator_object.name, parser_object)

		for code_snippet in translator_object.code_snippets:
			self.add_code_snippet(translator_object.name, code_snippet)

	"""
	Adds a mindsketch_parser.ParsreObject to a the translator object 'name'.
	Only meant to be called from 'add()'.
	"""
	def add_parser_object(self, name, parser_object):
		variables = set([var for var in parser_object if type(var) == mindsketch_parser.Variable])
		if self[name]["variables"] is None:
			self[name]["variables"] = variables
		elif variables != self[name]["variables"]:
			raise ValueError("All Parser Objects must use the same variables. Translator Object: " + name + ". " + str(variables) + " did not match " + str(self[name]["variables"]))

		self[name]["parser_objects"].append(parser_object)

	"""
	Adds a mindsketch_parser.CodeSnippet to a the translator object 'name'.
	Only meant to be called from 'add()'.
	"""
	def add_code_snippet(self, name, code_snippet):
		if code_snippet.language in self[name]["code_snippets"]:
			warnings.warn("Overwriting Code Snippet " + repr(code_snippet.language) + " for Translator Object " + repr(name))

		self[name]["code_snippets"][code_snippet.language] = code_snippet

	"""
	Validates all Translator Objects for consistent variable usage.
	Raises any errors as they are found.
	"""
	def validate(self):
		for name in self: 
			if self[name]["variables"] is None:
				raise ValueError("No Parser Objects have been defined for Translator Object: " + repr(name))
			
			# Validate that each code_snippet has at least one 
			for code_snippet in self[name]["code_snippets"].itervalues():
				left_over_vars = code_snippet
				for var in self[name]["variables"]:
					if var not in code_snippet:
						raise ValueError("Didn't use all variables in Translator Object: " + name + " in Code Snippet for: " + code.language)

				# It might be a typo if there are any varialbe-like strings left in the code snippet
				left_over_vars = set(mindsketch_parser.variable.findall(code_snippet)) - self[name]["variables"]
				if len(left_over_vars) > 1:
					warnings.warn("Possibly undefined variable(s): " + str(left_over_vars) + " in Translator Object: " + name + " in code snippet for: " + code_snippet.language, SyntaxWarning)


	"""
	Returns a list of output_lines for all the Translator Objects, comments included
	"""
	def output_lines(self):
		output_lines = []
		for name in self:
			output_lines.extend(self.output_translator_object(name))
		return output_lines


	"""
	Helper method for output_lines() that generates all the output lines
	for one Translator Object
	"""
	def output_translator_object(self, name):
		output_lines = ["# Translator Object: " + name + "\n"]
		output_lines.extend(["#" + comment + "\n" for comment in self[name]["comments"]])
		output_lines.append("\n")
		for parser_object in self[name]["parser_objects"]:
			output_lines.extend(self.output_parser_object(name, parser_object))
		for code_snippet in self[name]["code_snippets"].itervalues():
			output_lines.extend(self.output_code_snippet(name, code_snippet))
		output_lines.append("\n")
		return output_lines

	"""
	Helper method for output_translator_object(name) that generates
	all the output lines for an individual Parser Object
	"""
	def output_parser_object(self, name, parser_object):
		output_lines = ["#" + comment + "\n" for comment in parser_object.comments]
		
		parser_str = "parsers.add("
		parser_str += repr(str(name)) + ", "
		parser_groups = []
		for group in parser_object:
			if type(group) == mindsketch_parser.Variable:
				var_str = "(?P<" + group[1:] + ">.*?)"
				parser_groups += [repr(var_str)]
			else:
				parser_groups += [repr(group)]
		parser_str += "(" + ", ".join(parser_groups) + "))" + "\n"
		
		output_lines.append(parser_str)
		return output_lines

	"""
	Helper method for output_translator_object(name) that generates
	all the output lines for an individual Code Snippet
	"""
	def output_code_snippet(self, name, code_snippet):
		output_lines = ["#" + comment + "\n" for comment in code_snippet.comments]
		
		# Doubling curley braces escapes them for string formatting
		double_curly = code_snippet.replace("{", "{{").replace("}", "}}")

		for var in self[name]["variables"]:
			double_curly = double_curly.replace(var, "{0[" + var[1:] + "]}")

		code_str = "code_snippets.add("
		code_str += ", ".join([repr(str(name)), repr(str(code_snippet.language)), '"""' + double_curly + '"""'])
		code_str += ")" + "\n"
		output_lines.append(code_str)
		return output_lines

if __name__ == '__main__':
	main()
