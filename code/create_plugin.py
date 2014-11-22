import argparse, pypeg_parser, re, warnings
from pypeg2 import parse

def main():
	p = argparse.ArgumentParser (description="Creates a Sublime Text 3 plugin from the given .misk file.")
	p.add_argument("file", help=".misk file of Translator Objects")
	p.add_argument("output", help="file name to write to (inlude the file extension .py)")
	args = p.parse_args()

	with open(args.file, "r") as f:
		text = f.read() 

	ast = parse(text, pypeg_parser.MindSketch)
	output_lines = []
	for translator_object in ast:
		name = repr(str(translator_object.name))
		output_lines += ["# Translator Object: " + name + "\n"]
		parser_str = "parsers.add("
		parser_str += name + ", "
		parser_groups = []
		variables = []
		for g in translator_object.parser:
			
			if type(g) == pypeg_parser.Variable:
				var = str(g)
				variables += [var]
				var_str = "(?P<" + var[1:] + ">.+?)"
				parser_groups += [repr(var_str)]
			else:
				parser_groups += [repr(str(g))]
		parser_str += "(" + ", ".join(parser_groups) + "))"
		output_lines += [parser_str + "\n"]

		for code in translator_object:
			double_curly = code.replace("{", "{{").replace("}", "}}")
			for var in variables:
				if var not in double_curly:
					raise ValueError("Didn't use all variables in Translator Object: " + name + "in code snippet for: " + code.language)
				double_curly = double_curly.replace(var, "{0[" + var[1:] + "]}")
			left_over_vars = pypeg_parser.variable.findall(double_curly)
			if left_over_vars:
				warnings.warn("Possibly undefined variable(s): " + str(left_over_vars) + " in Translator Object: " + name + " in code snippet for: " + code.language, SyntaxWarning)
			code_str = "code_snippets.add("
			code_str += ", ".join([name, repr(str(code.language)), '"""' + double_curly + '"""'])
			code_str += ")"
			output_lines += [code_str + "\n"]

		output_lines += ["\n"]

	with open("plugin_template.py") as f:
		output_lines.insert(0, f.read())

	with open(args.output, 'w') as f:
		f.writelines(output_lines)

if __name__ == '__main__':
	main()
