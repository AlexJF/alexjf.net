Title: Y Game
Logo: {static images/logo.png}
Project_Start: 2011/09
Project_Authors: Alexandre Fonseca, Pedro Luz
Project_Version: 1.0
Project_Status: Finished
Gallery:
    {static images/yboard.png}||4-ring game field
    {static images/yboard-winO.png}||Winning game by player O, connecting outermost rings of 3 different sections
Attachments:
    {static files/y-game.zip}||Source code and report


This project was created as an assigment for the Artificial Intelligence course
during my 5th semester at IST.

In this project we were tasked with the implementation of a modified version of
the Y game and respective AI in LISP.

<!-- PELICAN_END_SUMMARY -->

In this modified version, 2 players must try and unite the outer layers of the
3 game subfields (the entire game field is shown in an image below) through a
sequence of adjacent cells. The first player to do so wins. Cells are adjacent
if either they touch or one of the cells corresponds to the last position on a
third of the field for ring X and the second cells corresponds to the first
position on the next third on ring X + 1 (e.g. ring 3, position 2 is adjacent
to ring 4 position 4). Another one of the images below shows a winning
condition. This game is turn-based with the plays alternating between the 2
players. Unlike the original Y game, draws are possible in this modified
version.

The AI is based on alpha-beta pruning with an heuristic created incrementally
from 6 smaller heuristics.

To play the game, you must have a LISP implementation installed (the game was
tested with clisp).

1. In the same directory as the `G5.lisp` file, run the lisp interpreter (e.g: clisp).
2. In the interpreter command prompt type `(load "G5.lisp")` to load the game functions.
3. To start a game, type `(executa-jogo <number of rings> #'<player function1> #'<player function2> <CPU time for AI in seconds>)`.
    * `<number of rings>` determines the size of the field. In the images below a 4-ring field is shown.
    * `<player function1/2>` can either be `faz-jogador-manual` (for a human
      player) or `faz-jogador-automatico` (for an AI player). Thus you can play
      with a friend, play against the computer or watch a match between 2 AI
      players.
* For each play, you're expected to give the coordinates of the cell where you want to place your token: `<ring number> <position in ring>`.
    * `<ring number>` is between 1 and `<number of rings>`.
    * `<position in ring>` is between 0 and `3*<number of rings> - 1`.
    * The game field is shown as:

            *   *   *
            **  **  **
            *** *** ***
            ************

        Where the 1st line represents the innermost ring (with the first *
        representing position 0 inside this ring, second * position 1, etc...),
        the 2nd line the second innermost ring, etc... This is a direct mapping
        onto one of the fields shown in the images.

* At the end of the game, you get a display of the final field along with a message between `+--------------+`:
    * `EMPATE` means draw.
    * `VITORIA-O` means victory for the O player. `VITORIA-X` means victory for the X player.
