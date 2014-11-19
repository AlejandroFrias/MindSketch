```
white space = ? white space characters ?;
all characters = ? all visible characters ?;
space = " ";
newline = ? newline character ?;
letter = ? lower case letters ?;
word = { letter };
plain text = word, { space, word };
title = { all characters - ":" }, ":";

group = "(", plain text, {"|", plain text }, ")", ["?"];
variable definition = variable, "=", ( "ANY" | "NUMBER" );
regex = (group | word | variable defintion), { space, (group | word - "PARSER END" | variable defintion) };
parser = "PARSER START", newline, regex, newline, "PARSER END";

code snippet = { all characters } - "CODE END"
template = "CODE START:", space, word, newline, code snippet, newline, "CODE END"

translator = title, parser, { template };
grammar = { translator };
```
