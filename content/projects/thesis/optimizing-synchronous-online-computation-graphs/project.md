Title: Optimizing Synchronous Online Computation of Large Graphs
Logo: {static images/logo.png}
Project_Start: 2014/01
Project_Authors: Alexandre Fonseca
Project_Status: Finished
Attachments:
    {static "files/thesis.pdf"}||Master thesis report
    {static "files/presentation.pdf"}||Master thesis presentation

This was my master thesis project developed at Telefónica between January
and July 2014 with academic supervision from Universitat Politècnica de
Catalunya.

In this thesis, I try to exploit the idle times inherent to imbalances in the
BSP/Pregel execution model (used by Giraph) to speedup the computation of
large graphs. This is done in the context of a system being developed at
Telefónica called Realtime Giraph that enhances Giraph by providing a 
realtime incremental computation mode.

<!-- PELICAN_END_SUMMARY -->

The 3 mechanisms implemented to achieve the objective were:

* Pipelining of simultaneous event execution.
* Partition-level local synchronization.
* Vertex-level local synchronization.
