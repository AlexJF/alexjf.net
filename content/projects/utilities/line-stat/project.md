Title: Line Stat
Logo: {static images/logo.png}
Project_Status: Finished
Project_Version: 1.0
Project_Authors: Alexandre Fonseca
Project_Start: 2008/07
Gallery:
    {static "images/Main Window.png"}||Main Window
    {static "images/SearchDir Window.png"}||Search Directory Window
    {static "images/Report Window.png"}||Report Window
Attachments:
    {static "files/Line Stat.zip"}||Line Stat (Win32)
    {static "files/LineStat-src.zip"}||Line Stat (Source - Code::Blocks Project)


Line Stat is a simple application whose purpose is to give you a report
regarding the number of lines (normal, comment and empty lines) of the files
you select.

<!-- PELICAN_END_SUMMARY -->

It supports every kind of text file but it was only designed to analyze C
styled code where single-line comments begin with `//` and multi line comments
begin with `/*` and end with `*/` so it might give you inaccurate results if used
somewhere else.

It was developed in C++ using the wxWidgets framework.

*Changelog*:

* 1.0 (14/07/2008) - First Release
