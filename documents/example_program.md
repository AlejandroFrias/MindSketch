```
Basic for loop:

PARSER START
(generate|make)? (for)? loop from START=ANY to END=ANY
PARSER END

CODE START: java
for(int i = START; i < END; i++) {
    $C
}
CODE END

CODE START: python
for x in xrange(START, END):
    $C
CODE END
```
