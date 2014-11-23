import argparse, pypeg_parser, re, warnings
from pypeg2 import parse

def main():
	p = argparse.ArgumentParser (description="Creates a Sublime Text 3 plugin from the given .misk file.")
	p.add_argument("file", help=".misk file of Translator Objects")
	p.add_argument("output", help="file name to write to (inlude the file extension .py)")
	args = p.parse_args()

	with open(args.file, "r") as f:
		text = f.read() 

	ast = parse(text, pypeg_parser.MindSketch, args.file)
	output_lines = []
	variables_dict = dict()
	for translator_object in ast:
		name = repr(str(translator_object.name))
		output_lines += ["# Translator Object: " + name + "\n"]

		for parser_object in translator_object.parsers:
			(parser_str, variables) = parser2plugin(parser_object, name)
			if name in variables_dict and variables != variables_dict[name]:
				raise ValueError("Didn't use the same variables for all Parser Objects of Translator Object: " + name)
			else:
				variables_dict[name] = variables
			output_lines += [parser_str]

		for code in translator_object.code_snippets:
			double_curly = code.replace("{", "{{").replace("}", "}}")
			if name not in variables_dict:
				warnings.warn("No Parser Objects have been defined yet for Translator Object: " + name + " before the Code Snippet for: " + language, SyntaxWarning)
			variables = variables_dict[name] if name in variables_dict else []
			for var in variables_dict[name]:
				if var not in double_curly:
					raise ValueError("Didn't use all variables in Translator Object: " + name + "in code snippet for: " + code.language)
				double_curly = double_curly.replace(var, "{0[" + var[1:] + "]}")
			left_over_vars = pypeg_parser.variable.findall(double_curly)
			if left_over_vars:
				warnings.warn("Possibly undefined variable(s): " + str(left_over_vars) + " in Translator Object: " + name + " in code snippet for: " + code.language, SyntaxWarning)
			code_str = "code_snippets.add("
			code_str += ", ".join([name, repr(str(code.language)), '"""' + double_curly + '"""'])
			code_str += ")" + "\n"
			output_lines += [code_str]

		output_lines += ["\n"]

	with open("plugin_template.py") as f:
		output_lines.insert(0, f.read())

	with open(args.output, 'w') as f:
		f.writelines(output_lines)

# converst a parser object into the proper line of code for the plugin
def parser2plugin(parser_object, name):
	parser_str = "parsers.add("
	parser_str += name + ", "
	parser_groups = []
	variables = set()
	for group in parser_object:
		if type(group) == pypeg_parser.Variable:
			variables.add(group)
			var_str = "(?P<" + group[1:] + ">.*?)"
			parser_groups += [repr(var_str)]
		else:
			parser_groups += [repr(group)]
	parser_str += "(" + ", ".join(parser_groups) + "))" + "\n"
	return (parser_str, variables)

if __name__ == '__main__':
	main()
