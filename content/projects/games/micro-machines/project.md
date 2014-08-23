Title: Micro Machines
Logo: {static images/logo.png}
Project_Start: 2011/02
Project_Authors: Alexandre Fonseca, Pedro Luz, Inês Ranha
Project_Version: 1.0
Project_Status: Released
Gallery:
    {static images/mm1.png}||Main screen
    {static images/mm2.png}||Car selection
    {static images/mm3.png}||Start position
    {static images/mm4.png}||First curve and red powerup
    {static images/mm5.png}||Second curve, pepper shaker and cockroach
    {static images/mm6.png}||Fast-closing gate
    {static images/mm7.png}||Multiplayer
    {static images/mm8.png}||Night mode
Attachments:
    {static files/MicroMachines-Win32.7z}||MicroMachines - Windows 32bit binaries
    {static files/Micromachines-Src.7z}||MicroMachines - Source (VS2010)


This game was made for the course of Graphic Computation during my 4th semester
at Instituto Superior Técnico.

The aim of the game was to create a clone of the popular MicroMachines game in
3D using OpenGL and the provided CGLib which acts as a wrapper around GLUT.

<!-- PELICAN_END_SUMMARY -->

The game has both a single-player mode and a multi-player mode. In
single-player mode, you race by yourself and your objective is to minimize your
lap time. In multi-player mode, you can play with a friend on a shared keyboard
and your objective is to leave your opponent behind. When this happens, you
gain one point and car positions are reset. Once you get a 5 point advantage
over your opponent you win.

As you can probably tell by the pattern used in the background, the game is
played on the top of a kitchen table in a track made of wood. There are various
obstacles: static sugar cubes, pepper-throwing shakers, quick-closing gates and
roaming cockroaches. Each time you collide with an obstacle you may lose speed
(or stop altogether) and/or resistance. Once your car resistance gets to 0,
your car is reset and you won't be able to move for 3 seconds. Keep in mind
that once you complete a full lap you replenish some of your lost resistance.

The cars have a noticeable drift thus requiring some practice if you want to
master the curves. They also have a turbo mode if you feel it is not going fast
enough. You may choose from one of 3 different car models (keep in mind they
are not very balanced when playing against an opponent).

There are also 2 different power ups that appear on the track as rotating
coloured cubes. A green cube replenishes your car resistance and a red cube
prevents you from losing resistance for a small period of time.

Controls:

* Arrow Up/Down/Left/Right - Move the car of Player 1
* W/S/A/D - Move the car of Player 2
* End (Player 1) / Space (Player 2) - Turbo
* Enter (Player 1) / r (Player 2) - Reset car position (if you get stuck for
  example)
* n - Toggle night mode
* ESC/Return/Arrow Up/Arrow Down - Navigate menus/selections
