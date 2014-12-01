# Preliminary evaluation


### What works well? What are you particularly pleased with?

I was happy to be able to have a fully working language that compiles to a working plugin for Sublime Text 3. I'm proud that the I've made many things easier to do with regards to making a sublime plugin that takes English statements and outputs code snippets.

Extra bonus was learning about custom syntax highlighting for my language, making it easier to write up Translator Objects. I can see a lot of potential for the language's use to expand with just a couple more features and tweaks.

### What could be improved? For example, how could the user's experience be better? How might your implementation be simpler or more cohesive?

~~The first thing that bugs me the most and is also the most minor, is that the custom syntax highlighing slows down Sublim Text to near freezing. Probably a lot of recursion going on. It wasn't written very efficiently. I get around it using TextMate which handles it a bit better.~~ Fixed this, Yay.

Optional Parser groups aren't supported the way I want. Right now I took them out. I'm having trouble keeping the spaces write for the Parser Objects when there are optional groups. I thought optional spaces in the regex would solve this, but then some Parsers were capturing more than I wanted them to.

There are few more things I want. I want import statements to allow seperate files of Translator Objects to be easily put together. I think this will allow multiple people to collaborate on the same translation suite.

I also wnat to add some special commands for cursor movement. The first most important one will be a command that equates to the hitting the TAB button. The eventual goal of the language is to remove the keyboard altogether. With use of Sublime's snippet language, tab stops allow for some interesting composing of commands. But they require the TAB key to be pressed. Other cursor movement commands would be necessary for this final goal. Since I won't be reaching that goal (which also requires an extra layer or two on the front end use of the plugin, namely a speach to text converter), I probably won't get around to add any of these types of commands. So this first version of the language is just an aid to coding and does not yet replace the keyboard.

A lot of knowledge is needed by the users of the language. They need to know basic of regular expressions, some basics of Sublime Text's snippet language, and whatever language they are creating. The only part that bothers me is that it is Sublime Text specific even at the level of the MindSketch level because of the snippet language. Otherwise, the point of the language is for domain experts to collaborate together to make coding more accessible. Maybe I should have something about accessibility in my language name...


### Re-visit your evaluation plan from the beginning of the project. Which tools have you used to evaluate the quality of your design? What have you learned from these evaluations? Have you made any significant changes as a result of these tools, the critiques, or user tests?

I ended up reversing how I thought I would evaluate my progress. Researching implementation details to make sure it was possible what I wanted to do took much longer than expected. Then I got carried away making a prototype. I've since written all the kinds of tests I wanted and refactored the code to look nicer, catching some errors and generating ideas for later refactorings and additions on the way.

I've been using `unittest` for testing of my code and running them using `nose`. Also, per Paul's suggestion, I'm using Python virtualenv for creating a virtual environment. Now setting up the language and using it is stream lined. I've gotten a lot of ideas from critiques and other people's word for various tools to try as well as design choices for ease of use.

### Where did you run into trouble and why? For example, did you come up with some syntax that you found difficult to implement, given your host language choice? Did you want to support multiple features, but you had trouble getting them to play well together?

The first major difficulty was finding out what sort of target language I was going to have to allow for English text to code snippets. That took way longer than expected. ANd once I landed on a possible way to do it, there were still some tricky parts with the implementation of it. The fact that the target was Sublime Text plugins affected my language design choices greatly. I ended up going with a Python parser, `pyPEG`, to keep things in the same language (as Sublime plugins are python as well). I also used some fo Sublime's features in my own language, like the code snippets. I also emulated some of the design of regular expressions and made ample use of string formatters to get things the way I wanted. So many syntax decisions changed as I hit various implementation problems.

The second major one was picking a scope. I'm dealing with generating code for fully functional languages, so staying a DSL was difficult to be able to tackle such a goal. I had to decide that my DSL would not support nesting of commands. I initially wanted it to, but that proved beyond my scope and ability. I solved this in a different way. When a code snippet is inserted, where the cursor ends up is up to the writer of the Translator Object. So if a snippet is a function call that leaves the cursor inside the funciton, a new seperate command can generate yet a nother function call snippet inside of it. Nesting of code is handled is linearized in this way. With the ability ot allow the cursor to stop at multiple places in a code snippet with Sublime Text tab stops, the possiblities increase.

One other issue I'm having is that some languages require that names of certain things be capatilized in certain ways. Like Java classes have to start with a capital letter and have to spaces. Most names actually can't have spaces. Right now I just let it be and it may require the user of the generated plugin to know more about the language they're writing in than I'd like.

One fun syntax issue was defining a code snippet. Code snippets often are multiple lines and indentation matters. THey also have all kinds of nutty characters. I found having a start and end marker made parsing easier as well as reading the language.

Now I mostly have the good kinds of difficulty: choosing which features to implement next given the little amount of time left and deciding on a good language name. I'm not sold on MindSketch.

### What's left to accomplish before the end of the project?

I've mentioned some of the features I'd like. I think for this project, there is only one more feature I definately want to add. The import feature. I think that one feature is pivotal to allowing collaboration. There are a myriad of smaller tweaks that I will also probably implement. Things like allowing more flexibility in the Parser Objects, like ignoring case and ignoring apostrophes and punctuation. Basically, normal English sentences should be able to be entered and match more smoothly, but so should less grammatically correct sentences and with the same Parser. Example, the same Parser Object should match `"I can't."` and `"i cant"`. I think an automatic layer that removes these types of things would be good. There's a couple of other TODO's smattered around the code with small tweaks and ideas.

Not so much a feature, but more like support, I was thinking building a small library of Translator Objects for people to expand off of. It would make the learning curve easier to see many examples of what it could do.

If I get really ambitious for the final demo I might make a web front end that makes writing up the Translator Objects even easier. There would be a form to fill out for creation. And a list of already created Translator Objects that could be swlected to be inlcuded in your plugin. Maybe even whole translation suites. Probabbly won't get there. But a guy can dream right?

Somewhere on my list of things to do should be a way to handle variable names nicely. It would be cool to include some functionality that allows the variable taken in from the Parser Object to transformed in various ways depending on the code snippet. So when you create a class and call it "hello world" in the snippet it becomes `HelloWorld`, like how you'd expect for Java and other languages. Or nameing a function "hello world" could make it `hello_world` or `helloWorld` depending on the language. I've seen plenty of thing for the implementation. The tough part is how to include it and parse it in the MindSketch language without making it too complicated to use or read. Some easy way to tag a variable in a code snippet as camel case or underscore separated. I think it is doable. It's hard to figure out what my priorities should be since I know I won't have time for everything.

