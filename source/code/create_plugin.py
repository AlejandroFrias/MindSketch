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
import argparse, mindsketch_parser, re, warnings
from pypeg2 import parse

def main():
	p = argparse.ArgumentParser (description="Converts MindSketch (.misk) file into a Sublime Text 3.")
	p.add_argument("file", help=".misk file of Translator Objects")
	p.add_argument("output", help="file name to write to (inlude the file extension .py)")
	args = p.parse_args()

	# Read in the MindSketch file
	text = "COULD NOT OPEN FILE"
	try:
		f = open(args.file, "r")
		text = f.read() 
		f.close
	except Exception, e:
		raise e

	# Parse the MindSketch file into an AST
	ast = parse(text, mindsketch_parser.MindSketch, args.file)

	output_lines = []
	variables_dict = dict()

	# generate the plugin code for each Translator Object
	for translator_object in ast:
		name = repr(translator_object.name)

		# Create comments for the translator object
		output_lines += ["# Translator Object: " + name + "\n"]
		# TODO add the comments

		# Create the Parser Objects
		for parser_object in translator_object.parsers:
			(parser_str, variables) = parser2plugin(parser_object, name)
			# Assert that constistent variable names are used for the same 
			# Translator Object, no matter when declared
			if name in variables_dict and variables != variables_dict[name]:
				raise ValueError("Didn't use the same variables for all Parser Objects of Translator Object: " + name)
			else:
				variables_dict[name] = variables
			
			# TODO add the comments
			# Add in the plugin code for this Parser Object
			output_lines += [parser_str]

		# Create the Code Snippets
		for code in translator_object.code_snippets:
			# Doubling curley braces escapes them for string formatting
			double_curly = code.replace("{", "{{").replace("}", "}}")
			
			# It is good practice to have declared at least one Parser Object
			# before any Code Snippets. This way it can be checked that the correct 
			# variable names are being used.
			if name not in variables_dict:
				warnings.warn("No Parser Objects have been defined yet for Translator Object: " + name + " before the Code Snippet for: " + code.language, SyntaxWarning)
			variables = variables_dict[name] if name in variables_dict else []
			
			# Replace all the variables with string format equivilants
			# Also throw an error if not all the variabls are used
			for var in variables:
				if var not in double_curly:
					raise ValueError("Didn't use all variables in Translator Object: " + name + "in code snippet for: " + code.language)
				double_curly = double_curly.replace(var, "{0[" + var[1:] + "]}")
			
			# It might be a typo if there are any varialbe like strings left in the code snippet
			left_over_vars = mindsketch_parser.variable.findall(double_curly)
			if left_over_vars:
				warnings.warn("Possibly undefined variable(s): " + str(left_over_vars) + " in Translator Object: " + name + " in code snippet for: " + code.language, SyntaxWarning)
			
			# TODO add the comments
			# Add in the plugin code for this Code Snippet
			code_str = "code_snippets.add("
			code_str += ", ".join([name, repr(str(code.language)), '"""' + double_curly + '"""'])
			code_str += ")" + "\n"
			output_lines += [code_str]

		output_lines += ["\n"]

	# The bulk of the plugin work is boiler plate.
	with open("source/code/plugin_template.py") as f:
		output_lines.insert(0, f.read())

	# Create the plugin
	with open(args.output, 'w') as f:
		f.writelines(output_lines)

# Converst a parser object into the proper line of plugin code
# and returns a set of the variables that were found.
def parser2plugin(parser_object, name):
	parser_str = "parsers.add("
	parser_str += name + ", "
	parser_groups = []
	variables = set()
	for group in parser_object:
		if type(group) == mindsketch_parser.Variable:
			variables.add(group)
			var_str = "(?P<" + group[1:] + ">.*?)"
			parser_groups += [repr(var_str)]
		else:
			parser_groups += [repr(group)]
	parser_str += "(" + ", ".join(parser_groups) + "))" + "\n"
	return (parser_str, variables)

if __name__ == '__main__':
	main()
