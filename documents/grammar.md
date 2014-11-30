```
white space = ? white space characters ?;
all characters = ? all visible characters ?;
space = " ";
newline = ? newline character ?;
letter = ? lower case letters ?;
var letter = ? upper case letters ?;
word = { letter };

comment = "#", { all characters }, newline

name = { all characters - ":" }, ":";

group = "(", word, {"|", word }, ")", ["?"];
variable = "$", var letter, { [ "_" ], var letter }

regex = (group | word | variable ), { space, ( group | word - "PARSER END" | variable ) };

parser object = { comment }, "PARSER START", newline, regex, newline, "PARSER END";

language name = { ( letter | "." | "+" };
code snippet body = { all characters | "$C" | variable } (* just can't spell "CODE END" *)
code snippet = { comment }, "CODE START:", space, language name, newline, code snippet body, newline, "CODE END"

translator = { comment }, name, { parser object }, { code snippet };

grammar = { translator };
```
