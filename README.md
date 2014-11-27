# MindSketch

MindSketch is a DSL (Domain Specific Language) for creating translations from English to code. At this stage, it is specifically geared towards creating a Sublime Text 3 plugin that accepts English commands and outputs code snippets. The dream is to one day be able to dictate code and have the messy worries about syntax for particular languages not be a hinderance to coding or learning to code. With everyone's collaboration, useful translation suites can be made that incoorporate the main ideas of coding and convert them into something useful

## Dependencies
Sublime Text 3
Python 2.7.x
pip

### Installing Sublime Text 3

The generated plugin works for Sublem Text 3 only. It is in beta, but still very functional. It can be downloaded [here](http://www.sublimetext.com/3).

### Python

MindSketch relies on [Python](https://www.python.org/) 2.7.x. If your machine does not already have Python installed, you can [download it](https://www.python.org/downloads/) from the web. Though 3.4.x will probably also work, it is untested.

### pip

MindSketch uses [pip](https://pypi.python.org/pypi/pip)  to manage the various Python modules that it makes use of.  MindSketch's bootstrap script uses pip to ensure that all proper dependencies are installed. Credit to [Paul](https://github.com/PaulDapolito) for the idea to use bootstrap and pip in this way.

#### Installing pip

1. Download the [get-pip.py](https://bootstrap.pypa.io/get-pip.py) file.
2. Execute the following command (may require use of `sudo`): `python get-pip.py`

## Installing MindSketch

1. Clone the repository using `git`:

	`git clone https://github.com/AlejandroFrias/MindSketch.git`

2. In the root directory of the project, run the `bootstrap.sh` script (may require use of `sudo`):

	`./bootstrap.sh` or `sh bootstrap.sh`
	
## Usage Instructions

1. Write a MindSketch file. If you save it as a `.misk` and save the [MindSketch.tmLanguage](https://github.com/AlejandroFrias/MindSketch/blob/master/source/MindSketch.tmLanguage) file into Sublime Text 3's User folder in Packages, then helpful syntax highlighting will ensue. It is also TextMate compatible.

2. Run the following script with the file you just created and optionally an output file name. Default output is `mind_sketch.py` in the current directory.
  
  `./mind_sketch.sh <MindSketch file> [<output file>]`

  For help on usage: `./mind_sketch.sh -h`
  
  Sample Usage: `.\mind_sketch.sh examples\simple_example.misk`. This will create `mind_sketch.py` that looks identical to `examples\example_plugin.py`

3. Save the plugin into Sublime Text 3.

	Open Sublime Text 3
	
	Open up the packages folder from the menu: `Sublime Text -> Preferences -> Browse Packages`
	
	Save the file to the `User` folder. (This is the same folder to put the [MindSketch.tmLanguage](https://github.com/AlejandroFrias/MindSketch/blob/master/source/MindSketch.tmLanguage) file into in order to get syntax highlighting for `.misk` files 
	
	In Sublime `ctrl+``opens the Sublime console. Error messages can show up here for incorrect use of the plugin.


