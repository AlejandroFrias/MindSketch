"""Tests for Sublime Text 3 Plugin generation.

This set of test checks for proper parsing of individual elements
of the grammar.

@author  Alejandro Frias
@contact alejandro.frias@ymail.com
@version 2014.11.26
"""
import unittest
from source.code.create_plugin import TranslatorObjectList
from source.code.mindsketch_parser import recursive_parse

class TestCreatePlugin(unittest.TestCase):
	def setUp(self):
		self.proper_syntax = "source/test/resources/proper_syntax.misk"
		self.proper_syntax_expected = """# Translator Object: Title should handle spaces and Numbers23
# Comments for the Translator Object
#    Should handle multiple lines and preserve spacing
# An be parsable even with lines seperating them
# Multiple Translator Objects should be able to be parsed
# And they can have the same name without overwriting parsers
# But it could overwrite code snippets or add to them depending on 
# the language of the snippet

# Parser Objects should get comments
parsers.add('Title should handle spaces and Numbers23', (u'words', u'(and)', u'(some groups|groups of a kind|groups)', u'to', u'be', u'parsed', u'with', u'(?P<START>.*?)', u'and', u'(?P<END>.*?)', u'variables',))
parsers.add('Title should handle spaces and Numbers23', (u'whatever', u'(i|do)', u'(?P<START>.*?)', u'and', u'(?P<END>.*?)',))
# As well as Code Snippets
#    And the multi-line thing
code_snippets.add('Title should handle spaces and Numbers23', 'java', \"\"\"for(int i = ${{1:{0[START]}}}; i < ${{2:{0[END]}}}; i++) {{
    $0
}}\"\"\")
code_snippets.add('Title should handle spaces and Numbers23', 'python', \"\"\"for x in xrange(${{1:{0[START]}}}, ${{2:{0[END]}}}):
    ${{0:pass}}\"\"\")

"""
		self.mismatch_variables = "source/test/resources/mismatch_variables.misk"
		self.missing_variables = "source/test/resources/missing_variables.misk"
		self.no_parsers = "source/test/resources/no_parsers.misk"

	"""
	proper_syntax.misk has every syntax feature, so it should 
	parse and generate plugin code accordingly
	"""
	def test_proper_syntax(self):
		ast = recursive_parse(self.proper_syntax)
		translator_objects = TranslatorObjectList(ast)
		translator_objects.validate()
		print("".join(translator_objects.output_lines()))
		print("****************")
		print(self.proper_syntax_expected)
		self.assertEqual("".join(translator_objects.output_lines()), self.proper_syntax_expected)

	"""
	Expect a ValueError when the parsers don't use the same set of variables
	"""
	def test_mismatch_variables(self):
		ast = recursive_parse(self.mismatch_variables)
		self.assertRaises(ValueError, TranslatorObjectList, ast)

	"""
	If a code snippet didn't use all the variables from the 
	parser, then something probably went wrong.

	TODO: Think about this. It might be possible to have optional
	      variables. Or variables that you capture that aren't used
	      for certain languages. The formatter can take extra and still
	      work fine. Then this could be a warning instead...
	"""
	def test_missing_variables(self):
		ast = recursive_parse(self.missing_variables)
		translator_objects = TranslatorObjectList(ast)
		self.assertRaises(ValueError, TranslatorObjectList.validate, translator_objects)


	"""
	There is no function in a Translator Object with no parser objects.
	
	TODO: Think about this. It is possilbe to have a sort of built 
		  in library of objects with code snippets that just need the 
		  parsers made. This could be a really good functionality.
		  Again, maybe move this to a warning
	"""
	def test_no_parsers(self):
		ast = recursive_parse(self.no_parsers)
		translator_objects = TranslatorObjectList(ast)
		self.assertRaises(ValueError, TranslatorObjectList.validate, translator_objects)
