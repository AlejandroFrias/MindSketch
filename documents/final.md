# MindSketch

Have you ever wished you could dictate your code? Or maybe you would like to write down psuedo code that actually translates into usable code without having to remember every syntax detail of whatever particular language you are writing in. Maybe you're a teacher and want to provide a way of coding that involves just the concepts and none of the language specific syntax features? Well MindSketch is a language designed to get us one step closer to being able to dictate in plain English and have that convert to proper code and code navigation.

I think I've convinced you of the need for such a final goal. It benefits everyone who wants to program. It helps experts who want to dictate. It helps those with injuries or blindness who want better accessibility features for handsfree coding. It helps those trying to learn or teach coding who work better in their native language than that of the computer. So what exactly does MindSketch do towards this goal?

MindSketch is a simple language for creating translations from English to code snippets. Currently this language compiles to a Sublime Text 3 plugin. The plugin accepts English sentences as input and outputs the corresponding code snippets or runs Sublime commands for navigation in the code. Using the Speech-to-Text accessibility feature built into your computer, you can get a taste of what it will be like to dictate your code.

Experts in various languages can collaborate on creating Translation suites for various languages. Those who are not experts can help create the English statements that should be used. The parts can be combined using import statements. It is meant as a collaborative project for creating English-to-Code translations.

The Translation suites don't have to be general purpose. I think this language has a lot of power for making psuedo DSL's in English. If the code snippets are more involved and more conventions are enforced on the user of the plugin, it can save them a lot of time. The possibilities are endless.

Please follow the instructions on the [README](https://github.com/AlejandroFrias/MindSketch/blob/master/README.md) for installation and use (there is also a tutorial).

## Design of MindSketch

Code snippets or code templates are very popular in many text editors and IDE's. They speed up programming. Allowing use of those but from text that represents the idea rather than the code snippet allows for better teaching tools and accessibility. It could even assist experts who want further abstraction from the workings of the computer to be able to deal with the ideas and concepts more directly. One could concieve of using MindSketch to create mini English DSL's for coding in various domains.

There are two stages of using MindSketch. Stage one is creating `.misk` files. Stage two is using the plugin that is generated from them.

See the [README](https://github.com/AlejandroFrias/MindSketch) for a tutorial on how to use this language.

### Stage 1: Write MindSketch Files

MindSketch files have Translator Objects defined in them as well as Commands. Translator Objects are translations from English to code snippets. Commands are translations from English to Sublime comands, mostly for code navigation purposes.

Multiple files can be merged together using `import` statements at the top fo the file.

To assist users in writing these files, syntax highlighting is available. The README also has instructions on how to use the [MindSKetch Syntax Grammar](https://github.com/AlejandroFrias/MindSketch/blob/master/source/MindSketch.tmLanguage) in Sublime.

#### Translator Objects

Translator Objects are written in `.misk` files. They follow the [MindSketch grammar](https://github.com/AlejandroFrias/MindSketch/blob/master/documents/grammar.md).

```
# This is a Translator Object named 'For loop'
For loop:

# It has one Parser Object that accepts phrases like 'loop from 1 to 4'
PARSER START
loop from $START to $END
PARSER END

# It has one Code Snippet for the python language.
# This is in the style of Sublime code snippets, taking advantage of tab stops
# Tab stops have two forms: $<number> and ${<number>:replacement text}.
# For details see Sublime Text's API
CODE START: python
for ${1:x} in xrange(${2:$START}, ${3:$END}):
	${0:pass}
CODE END
```

Every declaration of a Translator Object starts with its name. When the same name is used again it just adds the extra Parser Objects and Code Snippets to the same Translator Objet and overrides the Code Snippets for the same language. This means some `.misk` files can be just Parser Objects and others just Code Snippets to allow for switching out translations. An example of this switch can be seen in (code_snippets.misk)[https://github.com/AlejandroFrias/MindSketch/blob/master/examples/code_snippets.misk] and (parser.misk)[https://github.com/AlejandroFrias/MindSketch/blob/master/examples/parsers.misk]. As you can see in (parser.misk)[https://github.com/AlejandroFrias/MindSketch/blob/master/examples/parsers.misk], an `import` statement can be used to compose multiple MindSketch files.

##### Parser Objects

```
PARSER START
(for loop|loop) from $START to $END
PARSER END
```

Parser objects are very simple. It's all lower case words. Groups with choices can be used too, like `(for loop|loop)` which signifies that `for loop` or `loop` are acceptible inputs there. Variables are all caps and start with a `$`. The contrast makes it easy to read which helps make them easier to write and modify. The `$` makes it easier to implement and thereby give useful error messages, like when Parser Objects for the same Translator Object don't use the same set of variables.

##### Code Snippet

Code Snippets are language dependent. The example above has just one snippet for `python`. This means that the code snippet will only be used when working in a python file. Others can be added for other languages.

Code Snippets can have anything in them. The parts that aren't directly inserted raw are the variables and tab stops or fields. Variables have the same syntax as they do in Parser Objects, `$ALL_CAPS_AND_NUMBERS_2`. Anything captured by them from the user input is directly substitued into the Code Snippet. If the Code Snippet doesn't use the same set of variables as the Parser Objects, a ValueError is thorwn (or a warning if there are extra).

Tab stops/fields are a Sublime Text feautre that I've take advantage of in MindSketch. You can see documentation on them (here)[http://sublimetext.info/docs/en/extensibility/snippets.html]. Since MindSketch was developed to be used for Sublime Text 3 plugins, some of its features, like the Code Snippet, are specific to the Sublime Text.

#### Commands

* Note * This feature is new and not fully tested.

Commands, like those found [here](https://github.com/AlejandroFrias/MindSketch/tree/master/examples/navigation_commands.misk), basically binds a Parser Object to a Sublime command, rather than to a Snippet. `next_filed` and `prev_field` are useful for moving between tab stops created from the Code Snippets. The Navigation Command can bind to any Sublime command, even those defined in your own custom plugins. An example of that is the `convert_to_snake` that is a case converter from a plugin downloaded from [CaseConversio](https://github.com/jdc0589/CaseConversion).

They look like this:

```
COMMAND: next_field
(next|next field|ok)
COMMAND END
```

This Command accepts `next` or `next field` or `ok` as input and will execute the `next_field` command.

Commands are used to help fully elimnate the need for the mouse or keyboard, as navigation commands, search commands, find and replace, movements of selection, etc. can all be bound to English statements.


### Stage 2: Sublime Text 3 Plugin

Once you've written some MindSketch files, it's time to create the Sublime Text 3 plugin. Again, in depth instructions and a tutorial video are available on the (README)[https://github.com/AlejandroFrias/MindSketch/blob/master/README.md]. Creating the plugin and setting up is pretty straightforward, as is the use of it. Simply run the plugin with the key you chose to bind to it, type in an English command, and watch a code snippet appear where your cursor was. Hit tab to move along the tab stops and repeat.

## Implementation Overview and Process

As explained there the two main parts to MindSketh. The MindSketch files themselves, which are lists of Translator Objects, and the Sublime Text 3 plugin that is generated from them.

The first step in implementation of MindSketch was to find a text editor or IDE that I could write plugins for that can take in user input and insert code or move the cursor. Sublime Text 3 was a good candidate for this proof of concept. It doesn't have very much overhead creating and using plugins compared to a full IDE like Eclipse, but it still had enough features to be sufficiently useful for its purposes.

After creating a working plugin, I found I could create some (boiler plate plugin code)[https://github.com/AlejandroFrias/MindSketch/blob/master/source/code/plugin_template.py]. Refactoring it, I found I wanted to use the `collections` module that wasn't supported by the version of python that Sublime Text 2 ships with. Rather than requiring users to change their environment, I decided to use Sublime Text 3, which is in beta.

Since Sublime Text plugins are written in python, it made sense to continue to use python for the rest of the project. The plugin works be creating regex's from the Parser Objects to match agains the user input. The same regex also extracts the variables. Then string formatting is used to substitute the variables into the code snippets. Sublime has ways of checking the file type of an open file (or view), and this is used to determine which Code Snippet to use.

Given that the plugin was written in python, it made sense to write the parser for MindSketch in python as well. There would be less setup required this way. MindSketch itself is it's own external language, though, because it separates the implementation details from the concept better that way.

I used pyPEG2 to parse MindSketch files an turn them into useful Abstract Syntax Trees. It generates a python list of Translator Objects that have all the attributes easily accessible. The list can be easily used to being generating the plugin code.

The whole project is bundled using virtualenv. A `bootstrap.sh` script in the project root directoy installs all the 3rd party modules that are used. Then the `mindsketch.sh` script uses those the virtual environment just created for the running of plugin creation. This stream lines the process for users.

Testing is done with python's `unittest` module. By running `nosetests` from the root directory, all the tests are run.

#### Parsing

The (MindSketch parser)[https://github.com/AlejandroFrias/MindSketch/blob/master/source/code/mindsketch_parser.py] is a fairly simple file. At the top of it is the grammar that is being followed. PyPEG does a lot of work for me, like automatic whitespace detection. Also, the AST objects are subclasses of pythons types, making them immediately usable. It doesn't hand recursive decent parsing very well, but that was going to be a tough problem with MindSketch anyways. It is very difficult to seperate out what nesting is going on in such context free language. The way I solved this is with the tab stops and allowing people to insert snipets anywhere. Since the final plugin is used as an aid, there is no need to parse use input as an entirely complete language.

The parser will throw somewhat difficult messages to read if there are syntax errors, which is why there is a helpful custom syntax highlighting. It is difficult to give accurate line numbers to Syntax Errors, especially when imports are used. But it will give some kind error when there is this kind of issue.

#### Create Plugin

The (create plugin)[https://github.com/AlejandroFrias/MindSketch/blob/master/source/code/create_plugin.py] file does the bulk of the work of organziing the Translator Objects. Within that file there is a very robust class called TranslatorObjectList that subclasses an ordered dictionary. It does several things. First, it uses the parser to recursively parse the file and its imports, compsing them together into a raw list of Translator Objects. It takes tthat raw list groups all the Translator Objects together that have the same name. Then it validates the values used. So ValueErrors are raised when Parser Objects don't use the same variables or Code Snippets are missing some variables. It also raise warnings for possible errors, like when a Code Snippet has an extra variable like string in it that doesn't match the Parser Objects. These error messages are very useful.

The (plugin template)[https://github.com/AlejandroFrias/MindSketch/blob/master/source/code/plugin_template.py] is organized in such a way that it is generic for any plugin. The only change is that at the end of the file Parser Objets and Code Snippets can be added to two data structures that are essentially ordered dictionaries. The plugin template's design and structure is what keeps the parsering and code generation simple. It also gives some good user feed back during the use of the plugin. If a command that doesn't match any Parser Objects is entered, the text is just inserted raw and an error is printed to the Sublime Console. If a command that does match a Parser Object but there isn't a Code Snippet for the language the file is in, the error is inserted directly at the cursor.


## Evaluation

### How close to the Dream?

The dream is dictating code. With use of the accessibility Speech-to-Text software that comes with most OS's, we can get a taste of that dream. MindSketch will still need a better voice-to-text layer than that. Since MindSketch can bind to any plugin commands in Sublime, we just need to develop some code navigation commands that understand scope. The project is intended to allow a lot of collaboration on making usefule translation suites and usefule cammands. To assist in that I'd like to make an online database and frontend for the translation suites and commands.

MindSketch is a working proof-of-concept prototype. It is easily installed and used. It may not be particularly useful, since using Sublime Snippets directly is probably faster. That's ok, though. The important part was writing a language that allows collaboration on translations.

I supplied one interesting way to tackle the problem of recursive decent parsing of plain English. I just don't recurse. If the user inputs `if x less than 3 do return 1 otherwise return call to fib on num minus 1 plus call to fib on num minus 2`, Only the if statement is recognized and the rest of the pieces are just inserted as is in the various fields of the code snippet. Then with the use of tab stops, the user can navigate to each section and use the plugin again to parse the various sections. The basic idea is that the user decides where the recursive parsing of their own sentence occurs. The plugin isn't parsing a whole language.

