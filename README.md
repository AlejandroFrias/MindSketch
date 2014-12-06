# MindSketch

MindSketch is a DSL (Domain Specific Language) for creating translations from English to code. At this stage, it is specifically geared towards creating a Sublime Text 3 plugin that accepts English commands and outputs code snippets. The dream is to one day be able to dictate code and have the messy worries about syntax for particular languages not be a hinderance to coding or learning to code. With everyone's collaboration, useful translation suites can be made that incoorporate the main ideas of coding and convert them into something useful

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
1. Try an example fromm by following this tutorial [![Tutorial](http://img.youtube.com/vi/MfIa4mPY6TQ/0.jpg)](http://www.youtube.com/watch?v=MfIa4mPY6TQ)

2. Create a key binding for miind_sketch.

	In the menu open up `Sublime Text -> Preferences -> Key Bindings - User`.

	Paste this in there `{ "keys": ["super+shift+m"], "command": "prompt_mind_sketch" }` (for Windows change `super` to `ctrl`)

3. Write your own MindSketch file. If you save it as a `.misk` and save the [MindSketch.tmLanguage](https://github.com/AlejandroFrias/MindSketch/blob/master/source/MindSketch.tmLanguage) file into Sublime Text 3's User folder in Packages, then helpful syntax highlighting will ensue (end of tutorial video)

4. Run the following script with the file you just created and optionally an output file name. Default output is `mind_sketch.py` into your User Package in Sublime Text 3 (only works on OSX after default installation of Sublime Text 3.
  
  `./mind_sketch.sh <MindSketch file> [<output file>]`

  For help on usage: `./mind_sketch.sh -h`
  
  Sample Usage: `.\mind_sketch.sh examples\example.misk`. This will create `mind_sketch.py` that looks identical to `examples\example.py` and save it save it to the User Package for Sublime Text 3 (which will load the plugin)

5. Save the plugin into Sublime Text 3 if you didn't use the default

	Open Sublime Text 3
	
	Open up the packages folder from the menu: `Sublime Text -> Preferences -> Browse Packages`
	
	Save the file to the `User` folder.
	
	In Sublime `ctrl+``opens the Sublime console. Error messages can show up here for incorrect use of the plugin.




