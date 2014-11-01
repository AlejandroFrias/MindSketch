# Project description and plan

## Motivation

The dream is to be able to do hands free coding. I think it would be really cool to be able to walk around the room while I "write" my program simply with commands. As I code, in any language, I am already saying in my head what I should be writing. So I want a DSL that does the translation from idea to actual code for me. This means the same thoughts and constucts can be used to write code in virtually any language.

There some other motivations beyond the personal, such as a great teaching tool and a tool for the blind. The whole dream is really big, but for now I'm focused on creating a DSL that can be used to create translations from plain English text into code and other commands for text editing.

## Language domain

It's focused on text editing and parsing english. The DSL should provide the ability to create parsers for plain English (or any language that uses the same alphabetic characters) into code snippets and cursor navigation commands.

## Language design

Design described in one sentence: English commands that stream line the text editing part of coding.

The final running of the program will involve inputting english strings (or sentences) that immediately execute as a cool text editing command. Maybe the input is "generate main function" that the result is a code snippet of a Java main function and places the cursor on the first line of the body. Or perhaps the input is "define body of main method" that simply places the cursor in the body of the main method.

Lots of things can go wrong. Like keeping track of tabs for properly formatted results. Or how to find a function with a user defined name that has multiple words camel cased together as one when the input is a simply lower case string. I could enforce certain conventions or allow the user to define conventions for these kinds of things, but that might still be too limiting when one wants to code with a mix of convetions or randomly leave convention.

Errors will be difficult. The most common one will probably be that the English command given as input didn't have a defined translation. If the translations aren't made in such a way as to capture many different ways of saying the same thing, then it becomes very clunky to use. And I think it will be hard to give good error messages. Also, the idea is that the DSL itself gives users the ability to make their own translations. There could be translation suites made by different people. It will be hard to give useful feedback when the different translations have bad interactions. Or even within one translation if there are any confilicts. Like one phrase is ambiguous on how it should be parsed, or one regex captures everything that another does, making that one never useful.

The thoughts I'm having on how to limit the errors and problems is to limit the scope of the project. I'll start with a language that has a lot of boiler plate code I hate typing, probably Java, and start creating a parser for English commands into Java code and cursor navigation commands. Compile a list of the kinds of features the parser/translater part needs, so I get an idea of what is needed. And then see how I can enforce a lot of things. Like probably enforce camel case naming and use existing language features to give errors when one parser captures the entirety of another and how to assign priority and things like that

## Example computations

Input: generate class hello world

Output: (the bar | is where the cursor is after the command
public class HelloWorld {
    |
}

Input: generate main class

Output:
public class HelloWorld {
    public void static main (String[] args) {
        |
    }
}

Input: print hello world to console

public class HelloWorld {
    public void static main(String[] args) {
        System.out.println("hello world");
        |
    }
}

So on and so forth. There are lot of pieces in the background priding the cursor placement and what part of the command to grab and use in the snippet and how to use them. Other commands should include deleting parts or whole lines, renaming certain things globally and locally. Many of these kinds of things exist as part of IDEs. So one way to look at it is a English based navigation of the IDE's features, like Eclipses refactor -> rename feature and other such things. My DSL should allow the creation of English commands to execute those things that fancy text editor or IDE can do to one file.
