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

		self.mismatch_variables = "source/test/resources/mismatch_variables.misk"
		self.missing_variables = "source/test/resources/missing_variables.misk"
		self.no_parsers = "source/test/resources/no_parsers.misk"

		self.imports = []
		self.imports.append("source/test/resources/import_parsers.misk")
		self.imports.append("source/test/resources/import_both.misk")
		self.imports.append("source/test/resources/import_snippets.misk")
		self.imports.append("source/test/import_relative.misk")
		
		with open("source/test/resources/proper_syntax_expected.txt") as f:
			self.proper_syntax_expected = f.read()

		with open("source/test/resources/import_expected.txt") as f:
			self.import_expected = f.read()

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

	Though it is proper syntax, it is a ValueError when it comes time to making a plugin
	"""
	def test_no_parsers(self):
		ast = recursive_parse(self.no_parsers)
		translator_objects = TranslatorObjectList(ast)
		self.assertRaises(ValueError, TranslatorObjectList.validate, translator_objects)

	"""
	Test the import feature.

	Imports use relative paths, preserve ordering, and are recursively parsed.

	TODO: Do some smart stuff to avoid multiple imports of the same file and avoid cycles of imports.
	"""
	def test_imports(self):
		for importing_misk in self.imports:
			ast = recursive_parse(importing_misk)
			translator_objects = TranslatorObjectList(ast)
			translator_objects.validate()
			print("".join(translator_objects.output_lines()))
			print("****************")
			print(self.import_expected)
			self.assertEqual("".join(translator_objects.output_lines()), self.import_expected)
