Title: At Compiler
Logo: {static images/logo.png}
Project_Start: 2011/02
Project_Authors: Alexandre Fonseca, Pedro Luz
Project_Version: 1.0
Project_Status: Finished
Attachments:
    {static files/at.zip}||Compiler, source code and examples

This project was created as an assigment for the Compilers course during my 4th
semester at IST.

In this project we were tasked with the creation of a compiler for a new
language called at.

<!-- PELICAN_END_SUMMARY -->

Characteristics of at:

* 4 data types: integers, reals (with literals being expressed in scientific or engineering notation), strings and pointers.
* Global and local variable scopes.
* Stack variable allocation including arrays.
* C style comments.
* Supported operators: `- + # * / % ˆ = < > == >= <= != || &&  ̃ [ ] ? ( ) @`
* Pre-declarations with use.
* Symbol sharing with public.
* Functions. Calls made by name or @ to denote recursive calls.
* Conditionals: `[cond] # <true instruction>;` or `[cond1] [cond 2] ... [cond n] ? <true instruction> : <false instruction>` where `cond1`, `cond2`, ..., `condn` are checked in order as if `[cond1 && cond2 && ... && condn]*  was called.
* C-like iteration: `[ int i = 0; i < n - 1; i = i + 1 ] <instruction>`.
* Printing with `<symbol>!!`.

The compiler was implemented using lex for the syntax parsing, byacc for the
semantic parsing, C++ for the parsing of the syntax tree and code generation.
Generated code is valid i386 assembly.
