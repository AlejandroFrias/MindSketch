Critique for the Week of November 25th  
For Alejandro Frias  
By Jean Sung  

**My Attempts at Installing it**

I see that you had some partial instructions for downloading a working version, or at least preliminary working version of your language, and so I tried it. 
* Downloaded and installed Sublime Text 3
* Downloaded and installed Python 3.4
* Downloaded the `pypeg_parser.py`, `create_plugin.py`, `plugin_template.py`, `simple_example.misk` and put them in the same directory. 
* I followed the instructions in using the `create_plugin.py`
* I was able to get the input simple misk file to the sample output file, as shown here. 
![](http://i.imgur.com/KhzhMoW.png)

I did the saving output as a plugin and created the key binding but couldn't get the generate function for for loops to work. Here is where I got stuck:
![](http://i.imgur.com/zHrk5m6.png)

Error Message Checking
try running the create_plugin.py on a .misk file with typos and give me some feedback on the kinds of errors you would expect vs the ones you're getting.

* Missing a `START` 


```
PARSER 
(generate|make|create)? class $NAME
PARSER END

PARSER START
$NAME is a class
PARSER END
```

Resulting error message:
```
Traceback (most recent call last):
  File "create_plugin.py", line 70, in <module>
    main()
  File "create_plugin.py", line 13, in main
    ast = parse(text, pypeg_parser.MindSketch, args.file)
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pypeg2/__init__.py", line 649, in parse
    raise parser.last_error
  File "simple_example.misk", line 4
    (generate|make|creat
    ^
SyntaxError: expecting u':'
```

I would have expected for key words like START and END, that there would be an expected case some prompt for maybe what it expected. 

* Missing `java` 

```
CODE START: 
for(int i = ${1:$START}; i < ${2:$END}; i++) {
    $0
}
CODE END
```

Resulting error message:
```
// Nothing, it runs normally 
```

I would have expected at least a warning- it seems like this would cause problems down the line. 

* Missing `$0`

```
CODE START: 
for(int i = ${1:$START}; i < ${2:$END}; i++) {
    
}
CODE END
```

Resulting error message: 
```
//Nothing
```

Again, I would have expected at least a warning- it seems like this would cause problems down the line. 

These are some of the test cases I tried. Let me know if there are other specific actions I should try. I can also try more after I get the whole thing set up and working. 


**Feedback from design notebook**

Wow, you put in a lot of work this week and it seems like you've got a lot done- especially since last week seemed to be research and proof of concept code where this week seems to be a preliminary and working version. I saw a bit in class on Monday about where you are now and it was cool. I wasn't able to get it working on my computer, so maybe having an updated `README.md` file with instructions for downloading and installing (a step by step guide) may be helpful. 


