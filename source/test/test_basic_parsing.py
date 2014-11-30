"""Tests for MindSketch Parsing.

This set of test checks for proper parsing of individual elements
of the grammar.

@author  Alejandro Frias
@contact alejandro.frias@ymail.com
@version 2014.11.26
"""
import unittest
from source.code.mindsketch_parser import Comment, Variable, Word, \
						 Group, ParserObject, LanguageName, \
						 CodeSnippet, TranslatorObject
						 
from pypeg2 import parse, compose, some

class TestUnitComment(unittest.TestCase):
	"""Test Comment parsing
	
	Grammar:
		comment = "#", { all characters }, newline

	MindSketch comments are python style (starting with #).
	Parsing should capture all characters after the # as the comment
		(including all whitespace and empty string, minues the endline character,
		 minus the actual "#")
	"""

	def setUp(self):
		self.comment = "# A comment"
		self.extra_white_space = "#    So much whitespace    "
		self.empty_comment = "#"
		self.not_comment = "not a comment"
		self.tricky_not_comment = " # see it had whitespace at start of line"
		self.multiline = "# line 1\n# line 2"

	def test_comment(self):
		"""Test that simple comments are parsed correctly"""
		p = parse(self.comment, Comment)
		self.assertEqual(p, self.comment.replace("#", ""))
		
		p = parse(self.extra_white_space, Comment)
		self.assertEqual(p, self.extra_white_space.replace("#", ""))

		p = parse(self.empty_comment, Comment)
		self.assertEqual(p, self.empty_comment.replace("#", ""))

	def test_not_comment(self):
		self.assertRaises(SyntaxError, parse, self.not_comment, Comment)
		
		# Checks that leading whitespace isn't being included in parsed comment
		self.assertRaises(SyntaxError, parse, self.tricky_not_comment, Comment, whitespace=None)

	def test_multiline_comment(self):
		p = parse(self.multiline, some(Comment))
		expected = map(str, self.multiline.split("\n"))
		hashes = len(expected) * ["#"]
		blanks = len(expected) * [""]
		expected = map(str.replace, expected, hashes, blanks)
		self.assertEqual(p, expected)

class TestUnitVariable(unittest.TestCase):
	"""Test Variable parsing
	Grammar:
		var letter = ? upper case letters ?;
		variable = "$", var letter, { [ "_" ], var letter }

	"""

	def setUp(self):
		self.variables = []
		self.variables.append("$VAR")
		self.variables.append("$VAR2")
		self.variables.append("$VAR_THREE")
		self.variables.append("$VAR_3THREE_WAIT_FOUR")

		self.not_variables = []
		self.not_variables.append("VAR")
		self.not_variables.append("$1VAR")
		self.not_variables.append("$var")
		self.not_variables.append("$_VAR")

	def test_variable(self):
		for var in self.variables:
			print("TestUnitVariable.assertEqual for: " + var)
			p = parse(var, Variable)
			self.assertEqual(p, var)

	def test_not_variable(self):
		for not_var in self.not_variables:
			print("TestUnitVariable.assertRaises for: " + not_var)
			self.assertRaises(SyntaxError, parse, not_var, Variable)

class TestUnitWord(unittest.TestCase):
	"""Test Word parsing

	Grammar:
		letter = ? lower case letters ?;
		word = { letter };

	Words in MindSketch are all lower case words with no special chars.

	** TODO ** 
		Future versions will allow words with apostrophes and 
		ignore case. The final goal is for speech generated text
		to be used and many speech-to-text generators capatalize and 
		put in apostrophes. For the same reason, numerals (0, 1, 2...)
		and other punctuation may be included in later versions

	"""
	def setUp(self):
		self.words = []
		self.words.append("hello")
		self.words.append("world")
		self.words.append("z")
		self.words.append("Not")
		self.words.append("WORD")
		self.words.append("wOoD")
		self.words.append("can't")
		self.words.append("3")
		self.words.append("34")

		# Maybe one day..
		self.will_be_words = []
		self.will_be_words.append("34,002")
		self.will_be_words.append("$3.02")
		self.will_be_words.append("%25")

		# These are never words
		self.not_words = []
		self.not_words.append("$Hello")
		self.not_words.append("$VAR")
		self.not_words.append("this is multiple words")
		self.not_words.append("")
		self.not_words.append(" ")

	def test_word(self):
		for word in self.words:
			print("TestUnitWord.assertEqual for: " + word)
			p = parse(word, Word)
			self.assertEqual(p, word)

	def test_will_be_word(self):
		for will_be_word in self.will_be_words:
			print("TestUnitWord.assertRaises for: " + will_be_word)
			self.assertRaises(SyntaxError, parse, will_be_word, Word)

	def test_not_word(self):
		for not_word in self.not_words:
			print("TestUnitWord.assertRaises for: " + not_word)
			self.assertRaises(SyntaxError, parse, not_word, Word)
		

class TestUnitGroup(unittest.TestCase):
	"""Test Group parsing
	Grammar:
		group = "(", word, {"|", word }, ")", ["?"];

	Groups are of the regex style group. So in ()'s. They can be optional 
	with a '?' after them. Or is with '|'
	"""
	def setUp(self):
		self.groups = []
		self.groups.append("(simple)")
		self.groups.append("(two|choices)")
		self.groups.append("(multiple|choices|yup)")
		self.groups.append("(optional)?")
		self.groups.append("(optional|with|options)?")
		self.groups.append("(spaces too)?")
		self.groups.append("(spaces too|with groups)?")

		self.not_groups = []
		self.not_groups.append("()")
		self.not_groups.append("()?")
		self.not_groups.append("( )")
		self.not_groups.append("((nope))")
		self.not_groups.append("((no)|nesting)")
		self.not_groups.append("not|a|group")
		self.not_groups.append("nope")
		self.not_groups.append("(space is not|a| |word)")
		self.not_groups.append("(spaces only between words|not after )")
		self.not_groups.append("(spaces only between words| not before)")
	
	def test_group(self):
		for group in self.groups:
			print("TestUnitGroup.assertEqual for: " + group)
			p = parse(group, Group)
			self.assertEqual(p, group)

	def test_not_group(self):
		for group in self.not_groups:
			print("TestUnitGroup.assertRaises for: " + group)
			self.assertRaises(SyntaxError, parse, group, Group)

class TestUnitParserObject(unittest.TestCase):
	"""Test Parser Object parsing

	Grammar:
		parser object = { comment }, "PARSER START", newline, regex, newline, "PARSER END";
	
	A Parser Object a simple regex for accepting english commands
	"""
	def setUp(self):
		self.phrases = []
		self.phrases.append("simple phrase with only words")
		self.phrases.append("has (some)? (groups|regex groups)")
		self.phrases.append("has (some)? groups (and|as well as) $VARIABLES")

		self.comments = []
		self.comments.append("# A comment")
		self.comments.append("# A second comment")

		self.non_phrase = "cant have PARSER END"

	def test_parser_objects(self):
		for phrase in self.phrases:
			print("TestUnitParserObject.assertEqual for: " + phrase)
			p = parse(self.gen_parser_object(phrase), ParserObject)
			self.assertEqual(" ".join(p), phrase)

	def test_parser_objects_with_comments(self):
		for phrase in self.phrases:
			print("TestUnitParserObject.assertEqual for: " + phrase)
			po = self.gen_parser_object(phrase, self.comments)
			print("po: " + po)
			p = parse(po, ParserObject)
			print(p)
			self.assertEqual(" ".join(p), phrase)
			self.assertEqual(map(compose, p.comments), self.comments)

	def test_not_parser_object(self):

		self.assertRaises(SyntaxError, parse, self.gen_parser_object(self.non_phrase), ParserObject)
		for phrase in self.phrases:
			self.assertRaises(SyntaxError, parse, phrase, ParserObject)

	@staticmethod
	def gen_parser_object(phrase, comments=[]):
		comments = "".join([c + "\n" for c in comments])
		parser_object = comments + "PARSER START\n" + phrase + "\nPARSER END\n"
		return parser_object

class UnitTestLanguageName(unittest.TestCase):
	"""Test LanguageName parsing

	Grammar:
		language name = { ( letter | "." | "+" };

	This is the language that a code snippet is for. Currently you need to directly
	match the way Sublime categorizes them.

	Currently sublime does lower case words and short hand.

	e.g.
		python = Python
		java = Java
		cs = C# (C sharp)
		c++ = C++

	** TODO **
		Check for a subset of languages to allow and allow case insensitivity
	"""
	def setUp(self):
		self.languages = []
		self.languages.append("python")
		self.languages.append("java")
		self.languages.append("c++")
		self.languages.append("c")
		self.languages.append("objc")

		self.not_yet_languages = []
		self.not_yet_languages.append("Java")
		self.not_yet_languages.append("Python")
		self.not_yet_languages.append("Objective-C")
		self.not_yet_languages.append("JavaScript")

		self.not_languages = []
		self.not_languages.append("NEVER")
		self.not_languages.append("GONNA")
		self.not_languages.append("LET")
		self.not_languages.append("YOU GO")

	def test_languages(self):
		for lang in self.languages:
			print("TestUnitLanguageName.assertEqual for: " + lang)
			p = parse(lang, LanguageName)
			self.assertEqual(p, lang)

	def test_not_languages(self):
		for not_lang in self.not_languages:
			print("TestUnitLanguageName.assertEqual for: " + not_lang)
			self.assertRaises(SyntaxError, parse, not_lang, LanguageName)

class TestUnitCodeSnippet(unittest.TestCase):
	"""Test Code Snippet parsing

	Grammar:
		code snippet body = { all characters | "$C" | variable } (* just can't spell "CODE END" *)
		code snippet = { comment }, "CODE START:", space, language name, newline, code snippet body, newline, "CODE END"

	A Code Snippet is just that. A snippet that takes variables and tab stop in Sublime Text style.
	It also has a language that it is for
	"""
	def setUp(self):
		self.code_snippets = []
		self.code_snippets.append(("python", 'print("$MESSAGE")'))
		self.code_snippets.append(("java", 'System.out.println("$MESSAGE");'))
		self.code_snippets.append(("c++", 'printf("$MESSAGE");'))
		self.code_snippets.append(("java", 'for(int i = $START; i < $END; i++ {\n\t$0\n}'))

		self.comments = ["# ONE COMMENT", "# TWO COMMENT"]

		self.not_code_snippets = []
		self.not_code_snippets.append(("java", "Anything is ok as long as it doesn't have PARSER END in it. Oops."))
		self.not_code_snippets.append(("invlid language", "invalid language"))
		self.not_code_snippets.append(("$WHO?", "invalid language"))

	def test_code_snippets(self):
		for (language, snippet) in self.code_snippets:
			code_snippet = self.gen_code_snippet(snippet, language)
			p = parse(code_snippet, CodeSnippet)
			self.assertEqual(p, snippet)
			self.assertEqual(p.language, language)

	def test_code_snippets_with_comments(self):
		for (language, snippet) in self.code_snippets:
			code_snippet = self.gen_code_snippet(snippet, language, self.comments)
			p = parse(code_snippet, CodeSnippet)
			self.assertEqual(p, snippet)
			self.assertEqual(map(compose, p.comments), self.comments)
			self.assertEqual(p.language, language)

	@staticmethod
	def gen_code_snippet(snippet, language, comments=[]):
		comments = "".join([c + "\n" for c in comments])
		code_snippet = comments + "CODE START: " + language + "\n" + snippet + "\nCODE END\n"
		return code_snippet	

class TestUnitTranslatorObject(unittest.TestCase):
	"""Test Translator Object parsing

	Grammar:
		translator = { comment }, name, { parser object }, { code snippet };

	A Translator Object has a name, a list of Parser Objects, a list of Code Snippets,
	and some comments associated with it. The only required part is the name.

	e.g.

	# Comments for a translator object
	Name of a Translator Object:

	PARSER START
	a parser
	PARSER END

	CODE START: java
	a code snippet
	CODE END

	"""

	def setUp(self):
		self.comments = ["# Some comments", "# More comments"]

		self.phrases = []
		self.names = []
		self.names.append("Name3")
		self.names.append("Basic for loop")
		self.names.append("A title for a Translator Object")

		self.phrases.append("simple phrase with only words")
		self.phrases.append("has (some)? (groups|regex groups)")
		self.phrases.append("has (some)? groups (and|as well as) $VARIABLES")

		self.code_snippets = []
		self.code_snippets.append(("python", 'print("$MESSAGE")'))
		self.code_snippets.append(("java", 'System.out.println("$MESSAGE");'))
		self.code_snippets.append(("c++", 'printf("$MESSAGE");'))
		self.code_snippets.append(("java", 'for(int i = $START; i < $END; i++ {\n\t$0\n}'))

	def test_only_name(self):
		for name in self.names:
			self.check_translator_object(name)
			self.check_translator_object(name, comments=self.comments)

	def test_only_parser_objects(self):
		self.check_translator_object(self.names[0], phrases=self.phrases[:1])
		self.check_translator_object(self.names[0], phrases=self.phrases[:1], comments=self.comments)
		self.check_translator_object(self.names[0], phrases=self.phrases)
		self.check_translator_object(self.names[0], phrases=self.phrases, comments=self.comments)

	def test_only_code_snippets(self):
		self.check_translator_object(self.names[0], snippets=self.code_snippets[:1])
		self.check_translator_object(self.names[0], snippets=self.code_snippets[:1], comments=self.comments)
		self.check_translator_object(self.names[0], snippets=self.code_snippets)
		self.check_translator_object(self.names[0], snippets=self.code_snippets, comments=self.comments)

	def test_both(self):
		self.check_translator_object(self.names[0], phrases=self.phrases, snippets=self.code_snippets)
		self.check_translator_object(self.names[0], phrases=self.phrases, snippets=self.code_snippets, comments=self.comments)

	def test_switched_order_of_parsers_and_code_snippets(self):
		translator_object = """Name:

CODE START: java
sdlfkjsdlfkjsd
CODE END

PARSER START
asdasda
PARSER END
"""
		self.assertRaises(SyntaxError, parse, translator_object, TranslatorObject)


	def check_translator_object(self, name, phrases=[], snippets=[], comments=[]):
		translator_object = self.gen_translator_object(name, phrases, snippets, comments)
		p = parse(translator_object, TranslatorObject)
		self.assertEqual(p.name, name)
		self.assertEqual(map(compose, p.comments), comments)
		self.assertEqual(map(" ".join, p.parser_objects), phrases)
		(languages, just_snippets) = zip(*snippets) if snippets != [] else ([], [])
		self.assertEqual(p.code_snippets, list(just_snippets))
		self.assertEqual([c.language for c in p.code_snippets], list(languages))

	@staticmethod
	def gen_translator_object(name, phrases=[], snippets=[], comments=[]):
		comments_joined = "".join([c + "\n" for c in comments])
		code_snippets = "".join([TestUnitCodeSnippet.gen_code_snippet(language=snippet[0], snippet=snippet[1]) + "\n" for snippet in snippets])
		parser_objects	= "".join([TestUnitParserObject.gen_parser_object(phrase) + "\n" for phrase in phrases])
		translator_object = comments_joined + name + ":\n" + parser_objects + "\n" + code_snippets 
		return translator_object


if __name__ == '__main__':
	unittest.main()
