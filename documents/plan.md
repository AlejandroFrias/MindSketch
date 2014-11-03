# Project plan

## Language evaluation

I will have a series inputs that should be viable of my completed DSL that represent the different features involded. So generating code snippets, navigation of code, deleting code, refactoring/renaming pieces of code. Things like that. So there will be a test suite that shows progress.

During development I will also have a series of unit tests. Since the the language is itself only a DSL for creating the translations that the above described progress test suite will be testing (probably for English to Java). My DSL has the vocabulary for writing the translations. Each thing in the vocabulary will need tests. I know I will need vocabulary for direct english parsing, defining new commands, cursor movement, text searching (probably by regex) and possibly other features. A list of minimum features needed in the DSL for suporting the defintion of commands for the overall features (like code snippets and the others mentioned above) will be written. And corresponding unit tests will be made along side their development.

## Implementation plan

Week 1: Finish step 1. Start research for step 2 (since step 1 has already been started and research is a possible bottle neck)
Week 2: Start step 2. Start step 3 (being able to write up tests will help determine if a host language or execution plan is feasible)
Week 3: Continue steps 2 and 3. If things went smoothly in the research, possibly finish them. It seems likely right now that the steps involved in determining host language(s) and how exactly a program is run (and then creating a test suite for progress) is going to be tough. Possibly could spread out the development of the progress/showcase test suite with the development of the necessary features to allow starting on implementation sooner.
Week 4: Finish steps 2 and 3 (if not done already). Start on step 4 and if possible finish it (the first feature I believe will be the easiest, but since it is the first there will be a lot of initial setup, configuration, and other initial things that take extra time).
Week 5: Finish step 4. This would include testing it with a translation suite that passes the progress test (and is the beginning of building the final demo...)
Week 6: Start and finish step 5. This may require more research into text editors and execuation plan. But ideally I did that already and with the setup done from previous weeks, this feature should be able to be finished.
Week 7: Complete a working demo and final writeup. Ideally the demo is fakable to look like I'm saying my commands outloud, but the voice to text translation was done ahead of time. At this stage only the capabilities to generate code snippets and navigate a text file need to be completed. It is possible, if not likely, that it will only work for English to Java and not have been generalized yet to a DSL that can be used for doing any kinds of translations (user defined and for other languages), but that would be really cool and I'm going to aim for that. At the least though the vocabulary of English commands to Java code snippets and cursor naviagtion should be extendable within my DSL, if not by others, at least by me.

Stretch Goals: The two features generalized if not done so already. Adding the features described in steps 6 and 7 and then doing step 8 (making the language usable and extendable by others besides myself).

Super Stretch Goal (like basically Cafter graduating in December and looking for a project): Work on user experience and actually get it to a point that I can talk and things happen.


#### Steps
1. Write up the series of input to outputs (English to Java) that show the progression of features that I'll be able to support. So generating code snippets, cursor navigation, deleting code, renaming/refactoring code. The ultimate goal being enough features to showcase the possibility of full text editing capabilities in the form of English commands.
2. Determine host language, internal vs external, and as close to an excecution plan as I can without having the thing written. I'd like to have a very clear idea of how I'd write up an Enlgish to Java translation suite or trait or etc. in my DSL and how to use it. This might end up being very specific to a single text editor. Much research will need to be done here to determine different ways to input a string and then manipulate a text file accordingly. Hopefully something exists that can be modified or emulated.
3. Write up the test suite based off the input/output generated in step 1.
4. Add the capabilities required for English commands that generate code snippets and use the DSL to create a translation suite from English to Java that works for the first set of input/output tests generate in step 3.
5. Add the capabilities required for Enlgish commands that move the cursor for navagation in a text file. Use the DSL to create a translation suite for English commands to navigation of Java files that have proper Java syntax. Refactor as needed. Test against the input/output tests for progress.
6. Same as 4 and 5, but for deleting code.
7. Same as 4, 5, and 6, but for renaming/refactoring code.
8. This step may happen more than once in between steps 4-7, but will definately happen here. Refactor DSL and condense language where possible. Fix any patch jobs (or warts) that have been introduced thus far (within reason). The goal after this step is to have a usable DSL (by others beside the creator) for creating translation suites for more langauges than just Java. If it ends up it only works for Java, thats fine too. It would still be a significant step, and Java is large enough that there would still be benefits from allowing others to add to the vocabulary of the translation suites.
9. Ideally at this point the demo is working that takes in English commands and spits out code or other text editing commands, but probably the user experience is still clunky. The user experience is last on my list, but it would be really cool if I had time to work on smoothing this out.

## Teamwork plan 

N/A. working alone

*If applicable*
