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

#### How to use my DSL?





## Language implementation
