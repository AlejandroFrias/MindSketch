# Language design and implementation overview

## A Basic Overview of the DSL and how to use it

Write a translation suite that takes in English text and outputs code generation or code navigation. The DSL is designed to make this process as streamlined as possible. Basic parser combinators will be supplied that allow extraction of certain elements of an English statement and for allowing multiple ways to the say the same thing. Also, simple commands will be given for code navigation.

E.G.
```
FOR_LOOP:
  parse: "generate for loop from", start=NUMBER, "to", end=NUMBER, ("increment by", amount)?
  generate: """
  for (int i = <<start>>; i <= <<end>>; <<IF(amount) "i++" ELSE "i+="amount>>) {
    <<cursor>>
  }
  """
    
GO_TO_MAIN:
  parse: "go to main", ("method" | "function")?
  cursor: SEARCH("public static void main.*{")
```

This code will compile into a Sublime Text 2 plugin that opens up an text input layer when called (this can be bound to any key, like CRTL+m). Upon typing in a command that matches one of the command objects' `parse` sections, the corresponding code generation and cursor movement will occur.

With this example the command input `generate for loop from three to nine` generates the code:
```
for (int i = 3; i <= 9; i++) {
  |
}
```
It will place the cursor where the `|` is. Then normal typing can continue or another command can be issued for other code generation or navigation.

`NUMBER` is a built parser for English numbers. Other built ins like `NAME` will also be inlcuded. It is hopefully written in a way that users can extend the vocabulary of the DSL to include other parser objects and use them to build larger ones for more complicated sentences.

In the `generate` section, items between `<<` and `>>` will be replaced by the code. Variables and simple conditionals are enough to most of the basic code generation commands desired. If this is an internal language, the capacity of a full programming language might even be available for this. We'll see.

This is a first approximation of the desired syntax and input. Many changes are likely to occur during development and testing.

## Language design

#### How to write a program in my DSL?

Write the translation suite in a file with my DSL. Running program generates a Sublime Text 2 plugin (a .py file) that you can incoorporate in your Sublime Text 2 and add a shortcut key binding for. Essentially the file is compiled into the plugin.

#### What is the basic computational model?

My language is essentially a parsing language for plain text that also provides some cursor movement commands.

#### What are the basic data structures? How does a user create and manipulate data?

As showna above, the basic structures are Parser Objects. A parser object has a name, a parser, a code generator that can use pieces of what was parsed, and a cursor movement function that moves the cursor to the correct location after any code is generated. The objects are written out simply in a file. They are the only things in the file. All the rest of generating a user input layer in Sublime Text 2 and creating the proper comands for moving the cursor and inserting the generated code is taken care of in the compiling stage.

#### What are the basic control structures?

Simple conditional statements and variables will be used for code generation. Those are sufficient for most of the use cases. They are written inside of `<<` `>>`'s to distinguish them from the string that is the code to be generated.

Some basic regex and parsing capabilities are given, like option `?`, grouping `()`, or `|`, and `,` as seen in the above example. At least one `+`, Zero or more `*` will also be provided.

#### Inputs and Outputs?
For the DSL.

Input: Parser Objects
Output: Sublime Text 2 Plugin

For the resulting plugin.

Input: String (in English probably)
Output: Code generation and cursor movement in the Sublime Text 2 editor

#### Error Handling

Syntax errors would be the most common. These would occur when the DSL is run to generate the plugin. It shouldn't be too difficult to give useful error messages as to syntax problems.

Depending on the level of use that I allow and that users go to, it is possible more complex errors can occur when combing parsers. More likely errors can occur when parsers are ambiguous. This will be difficult to catch, both on the backend and for the user. I'm not sure how to handle this yet, and it will have to come later when I begin testing some working pieces.

Right now, the only way for error to be communicated are during the plugin generation phase and the only useful errors it can catch will likely be syntax errors rather than logic errors.

#### Tool Support

Further research is being conducted currently into other parsers that I might extend, in which case all the tool support for those langauges might be available to the user. I'm considering making it an internal language to open up features, but am weary of this decision. Need to write some more test programs.

#### Other similar DSL's?

There are many different parsers that exist. All the ones I have found supply to many other features that I don't need. Xtend is an interesting Eclipse plugin that has some great parser and code genteration, but it has a lot of overhead and requires Eclipse when the target is Sublime Text 2. Scala's Parsers seeem capable of what I want to do, so I may be using those in the backend.

Python has several interesting parsers, such as pyPEG, grako, and RE|PARSE. Since Sublime Text 2 plugins are written in python, it is likely that that the generated plugin will use one of these. In a way my DSL is a translation into one of these.

Basically there are many parsing DSL's that one can use to parse english, extract pieces from it, and generate a string with those pieces. That is at the core of hte implementation, what I'm doing. But the what is being generated is clunky and not made easy by any DSL's specifically the plugin generation. So I'll be making DSL that has a subset of the parsing features that these other parsing DSL's have, but provides easier to use features for generating the necessary plugin code for inserting the strings generated at the right place and for moving the cursor to the right place.

## Language implementation

#### Why external or internal?

I'm very torn on this matter. I think it will become more clear as I write out various Sublime Plugins that I want to be generated.

Ideally I'd find a parser that already exists that is easy to use. pyPEG or RE|PARSE might work. It's just one more layer to make the plugin code easy to generate. Functions like `SEARCH(regex)` that place the cursor at the next instance that the next instance the regex matches (with loop around). And each plugin will have some boiler plate code as well for the input layer. Again, I think it will made clear once I right some working Sublime plugins and then discover how best to generate those.

My feeling right now is that an external DSL will be easier to limit the capabilities of the language. All commercial use parsers have way more features than is needed for the this small subset of parsing.


#### Host language

I'm still open for suggestions. From what I've seen, I like the Scala language and it's parsers the best. It's likely that will be what I use to convert the file written in my DSL into the sublime Plugin (passing through an AST first of course). It may turn out that I can save implmention time if I do everything in python, so I'm waiting to decide this. I have plenty of python code to write to see what kind of information the AST will need to have in orger to generate the plugins from it. Most likely going to use Scala though.

#### Syntax decisions

Most of the syntax was inspired by other parsers, like pyPEG. I think I keep the syntax close to the what the plugin might look like I'll gain two benefits. One, it might be easier to write for me, the designer. Two, the users might be able to read the resulting plugin better, which can have intersting benefits for code savvy people who want to tweak it on the backend a little. Again, I need to write the sublime plugins themselves that are my target.

#### Overview of Architecture





