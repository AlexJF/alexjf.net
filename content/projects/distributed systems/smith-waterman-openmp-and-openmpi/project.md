Title: Smith-Waterman with OpenMP and OpenMPI
Logo: {static images/logo.png}
Project_Start: 2012/09
Project_Authors: Alexandre Fonseca, Anh Thu Vu
Project_Version: 1.0
Project_Status: Finished
Attachments:
    {static files/report.pdf}||Report
    {static files/ampp-g4-codes-scripts-outputs.tar.gz}||Code, tests, scripts and outputs


This project was created as an assigment for the Algorithms and Models for
Parallel Programming course during my 1st semester at UPC.

In this project we were tasked with the implementation of parallel versions of
the Smith-Waterman algorithm for sequence alignment using OpenMP and OpenMPI.

<!-- PELICAN_END_SUMMARY -->

We also had to develop theoretical models for the performance of the
parallelization and compare it with the results obtained through
experimentation with the actual implementation.

In the end, we presented our results for several different implementations of
the parallelization:

* OpenMPI without row-level interleaving.
* OpenMPI with row-level interleaving.
* OpenMP using tasks.
* OpenMPI + OpenMP.

For details about the implementation and evaluation, refer to the attached
report.
