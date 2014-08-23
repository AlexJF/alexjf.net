Title: GR8 Engine
Logo: {static images/logo.png}
Project_Start: 2008/06
Project_Authors: Alexandre Fonseca
Project_Version: 0.1
Project_Status: Postponed Indefinitely
Gallery:
    {static images/gr8-1.png}||Test App initial
    {static images/gr8-2.png}||Test App collision and movement
    {static images/gr8-3.png}||Test App ramp
Attachments:
    {static files/GR8Engine-Win32.7z}||GR8Engine Win32 Binaries
    {static files/GR8Engine-Src.7z}||GR8Engine Sources (VS 2010)

GR8 Engine is a C++ 2D game engine based in SDL and OpenGL.

When finished, GR8 Engine is supposed to be a simple but complete game engine
that provides all the functions and classes a game programmer might need.

<!-- PELICAN_END_SUMMARY -->

GR8 Engine also uses the Box2D Physics engine for accurate and realistic object
movement and collisions.

So far, it contains the following features:

* A screen manager that allows the coexistence of several game screens (such as
  the main menu, game screen and pause menu).
* An event manager that propagates events throughout the entire application.
* A control manager that handles the updating and drawing of controls. The
  currently implemented controls are labels, textboxes and buttons.
* A graphics class that is able to draw rectangles, circles, polygons, textures
  and text and contains useful functions such as FPS capping and cameras.
* A sound class that manages background music and sound effects.

Included on the packages below is a small test program where you can control a
football with the arrow keys. The map is divided in 3 areas by two big towers.
On the leftmost one, there's a small ramp with a tunnel beneath it. On the
center one there's a basketball with which you can interact. On the rightmost
one there's nothing.

The test app also contains two active controls: a textbox and a button. These
controls are draggable and function more or less as you'd expect from normal OS
controls. You click them to focus them (or activate in the case of the button).
They remain focused until you click somewhere else outside the control.

Note that I wrote most of the code before entering university and based on
self-learning. As such, some areas might be poorly implemented or engineered.
Also, I initially developed it using the MingW compiler and had to port it to
the VC++ compiler so this porting can have introduced some obscure bugs.
