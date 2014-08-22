Title: Datacenter Power-Aware Management Optimization
Logo: {static images/logo.png}
Project_Start: 2013/01  
Project_Status: Finished  
Project_Version: 1.0
Project_Authors: Alexandre Fonseca, Anh Thu Vu, Peter Grman
Attachments:
    {static "files/CNO - Project.zip"}||Project files
    {static "files/report.pdf"}||Report

This project was created as an assigment for the Computer Networks Optimization
course during my 2nd semester at UPC.

In this project we were tasked with the solving of an Integer Linear Program
(ILP) for Datacenter Power-aware Management using existing ILP solvers and
heuristic-based solvers we created ourselves.

For the 1st part, we used the model developed in [An Integer Linear Programming
Representation for DataCenter Power-Aware Management](
"http://upcommons.upc.edu/e-prints/bitstream/2117/11061/1/R10-21.pdf") and ran
it in 3 different ILP solvers: Gurobi, GLPK and CBC.

For the 2nd part, we developed 2 entirely custom heuristic frameworks, one in
C++11 (by me) and the other in C# (by Peter) with different characteristics
(more info on the paper below). Using these frameworks, we implemented 2 types
of heuristic solvers: one based on a combination of GRASP + TabuSearch + Path
Relinking and another based on Simulated Annealing with different solution
construction steps.

Based on collected results, we then evaluated the performance and accuracy of
the solvers and studied the effect of the different parameters on these
components.
