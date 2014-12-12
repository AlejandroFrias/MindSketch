# MindSketch

MindSketch is a DSL (Domain Specific Language) for creating translations from English to code. At this stage, it is specifically geared towards creating a Sublime Text 3 plugin that accepts English commands and outputs code snippets or executes a Sublime command. The dream is to one day be able to dictate code and have the messy worries about syntax for particular languages not be a hinderance to coding or learning to code. With everyone's collaboration, useful translation suites can be made that incoorporate the main ideas of coding and convert them into something useful!

## Dependencies
Make sure you have the following installed on your computer. I apologize that I haven't made this project very accessible to non-OSX.

* Sublime Text 3
* Python 2.7.x
* pip

### Installing Sublime Text 3

The generated plugin works for Sublem Text 3 only. It is in beta, but still very functional. It can be downloaded [here](http://www.sublimetext.com/3).

### Python

MindSketch relies on [Python](https://www.python.org/) 2.7.x. If your machine does not already have Python installed, you can [download it](https://www.python.org/downloads/) from the web. Though 3.4.x will probably also work, it is untested.

### pip

MindSketch uses [pip](https://pypi.python.org/pypi/pip)  to manage the various Python modules that it makes use of. Instructions for installing are [here](https://pip.pypa.io/en/latest/installing.html). MindSketch's `bootstrap.sh` script uses pip to ensure that all proper dependencies are installed. Credit to [Paul](https://github.com/PaulDapolito) for the idea to use bootstrap and pip in this way.

## Getting MindSketch

1. Clone the repository using `git`:

	`git clone https://github.com/AlejandroFrias/MindSketch.git`

2. In the root directory of the project, run the `bootstrap.sh` script (may require use of `sudo`):

	`./bootstrap.sh` (if it says permission denied, you may need to make it an executable with `chmod a+x bootstrap.sh` or run it with `sh bootstrap.sh`

## Usage Instructions

0. Install the depencies and clone the repo if you haven't already. run `bootstrap.sh` to make sure the 3rd party modules are installed.
1. Try an example fromm by following this tutorial (turn your volume up). [![Tutorial](http://img.youtube.com/vi/MfIa4mPY6TQ/0.jpg)](http://www.youtube.com/watch?v=MfIa4mPY6TQ)

2. Create a key binding for miind_sketch.

	In the menu open up `Sublime Text -> Preferences -> Key Bindings - User`.


	Paste this in there `{ "keys": ["super+shift+m"], "command": "prompt_mind_sketch" }` (for Windows change `super` to `ctrl`)

3. Write your own MindSketch file. If you save it as a `.misk` and save the  file into Sublime Text 3's User folder in Packages, then helpful syntax highlighting will ensue (end of tutorial video).

4. Run the following script with the file you just created and optionally an output file name. Default output is `mind_sketch.py` into your User Package in Sublime Text 3 (only works on OSX after default installation of Sublime Text 3.
  
  `./mind_sketch.sh <MindSketch file> [<output file>]`

  For help on usage: `./mind_sketch.sh -h`
  
  Sample Usage: `.\mind_sketch.sh examples\example.misk`. This will create `mind_sketch.py` that looks identical to `examples\example.py` and save it save it to the User Package for Sublime Text 3 (which will load the plugin)

5. Save the plugin into Sublime Text 3 if you didn't use the default

	Open Sublime Text 3
	
	Open up the packages folder from the menu: `Sublime Text -> Preferences -> Browse Packages`
	
	![Browse Packages](https://raw.githubusercontent.com/AlejandroFrias/MindSketch/master/documents/resources/browse_packages.png)

	Save the file to the `User` folder.

	![User Folder](https://raw.githubusercontent.com/AlejandroFrias/MindSketch/master/documents/resources/user_folder.png)
	
	In Sublime ``` ctrl+` ``` opens the Sublime console. Error messages can show up here for incorrect use of the plugin.

	![Sublime console](https://raw.githubusercontent.com/AlejandroFrias/MindSketch/master/documents/resources/sublime_console.png)

## Features

The [example](https://github.com/AlejandroFrias/MindSketch/blob/master/examples/example.misk) MindSketch file has all the features show cased and produces a usable Sublime Text 3 plugin.

#### Translator Objects

The basic translations look like this:

```
Loop:

PARSER START
loop from $START to $END
PARSER END

CODE START: python
for x in xrange($START, $END):
	$0
CODE END
```

They have a name, one or more Parser Objects and one or more Code Snippets. They are named so that in another file or later in the file you can add more Parser Objects or Code Snippets to the same Translator Object. More on that in the imports section.

Parser Objects match the English statements and commands that the generated Sublime plugin will receive as input. They grab variables out of the statements to use in the Code Snippets. You can also have groups with options like:

```
PARSER START
(for loop|loop) from $START to $END
PARSER END
```
This accepts `for loop from 1 to 10` as well as `loop from 1 to 10`, assigning variables `$START` and `$END` to `1` and `10`, respectively.

Code Snippets are Sublime style snippets. Check out their API [here](http://docs.sublimetext.info/en/latest/extensibility/snippets.html). They use all the same tab stops and placholder syntax as the Sublime snippet language. They also substitute in the values grabbed from the user input and assigned to the variables. Very importantly, you can have only one Code Snippet for each language and one default one. All are optional.

For the above Translator Object, the input `loop from 1 to 10` would produce `for x in xrange(1, 10)` with the cursor on the next line indented to the `$0`. It will only do this inside a python file though. The bottom right corner of the sublime window shows the file type recognized and it is a drop down menu that can be changed.

![Sublime View](https://raw.githubusercontent.com/AlejandroFrias/MindSketch/master/documents/resources/blank_sublime.png)


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


#### Imports

MindSketch files can import other mind sketch files.

```python
import other_file.misk
import other_file2.misk

...
```

Imports are always at the top of the file before anything else. When an imported file has Translator Objects with the same name, the Parser Objects and Code Snippets get merged into the same object. This allows users to make a file of just Code Snippets (or even mulitple with one for each language for example) and a file with just Parser Objects. This allows customization of Translation suites and collaborations.

Imports of Navigation Commands is also possible, as seen in the example.

Imports use relative paths and cycles will automatically be detected. No duplicates will be improted.

## Tools and Support

#### Syntax Highlighting

To get syntax highlighing, use the [MindSketch.tmLanguage](https://github.com/AlejandroFrias/MindSketch/blob/master/source/MindSketch.tmLanguage) file. It is TextMate compatible as well as Sublime compatible. For sublime copy the file into you User Package.

