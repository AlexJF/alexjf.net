Title: CFS sthreads + SNFS Extensions
Logo: {static images/logo.png}
Project_Start: 2010/09
Project_Authors: Alexandre Fonseca, Pedro Luz
Project_Version: 1.0
Project_Status: Finished
Attachments:
    {static files/so.zip}||Description, source files and tests

This project was created as an assigment for the Operating Systems course
during my 3rd semester at IST.

In this project we were asked to extend existing thread and file system
libraries to support new operations, working upon what we were taught during
class.

<!-- PELICAN_END_SUMMARY -->

It was divided in 2 parts:

* Extending an existing thread library (sthreads) so as to use the CFS
  scheduler employed by the Linux kernel 2.6.23 and adding a nice command. This
  required the implementation of a Red-Black tree.
* Extending a very basic file system called SNFS so as to support file removal,
  concatenation, copying, copy-on-write, block caching and defragmentation.

The project was implemented in C and functionality was implemented with a focus
on parallel execution, with synchronization blocks being created with
mutexes/monitors.
