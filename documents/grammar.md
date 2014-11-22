```
white space = ? white space characters ?;
all characters = ? all visible characters ?;
space = " ";
newline = ? newline character ?;
letter = ? lower case letters ?;
var letter = ? upper case letters ?;
word = { letter };
title = { all characters - ":" }, ":";

group = "(", word, {"|", word }, ")", ["?"];
variable = "$", var letter, { [ "_" ], var letter }
variable definition = variable;
regex = (group | word | variable defintion), { space, (group | word - "PARSER END" | variable defintion) };
parser = "PARSER START", newline, regex, newline, "PARSER END";

code snippet = { all characters | "$C" | variable } (* just can't spell "CODE END" *)
template = "CODE START:", space, word, newline, code snippet, newline, "CODE END"

translator = title, parser, { template };
grammar = { translator };
```
