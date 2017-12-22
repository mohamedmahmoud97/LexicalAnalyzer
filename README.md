# Compiler Lexical Analyzer Generator

#### It's a the first phase in the front end of the compiler.

- There are two input files, one for the grammar rules and one for the source code.
- The output is a list of tokens which matches the user's input file.

#### To run the code:

- Put your grammar in a file like grammar.lex with the same format and put your source file code in a file.
- Run the code with in the terminal in the directory of the project:

```
[uname@hostname JavaCompiler]$ python LexicalAnalyzer/__main__.py
Grammar file name: LexicalAnalyzer/grammar.lex
Code file name: LexicalAnalyzer/code.c
```

- Then the output will printed.