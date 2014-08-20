Title: An evaluation of the genome alignment landscape.  
Logo: {static images/logo.jpg}
Project_Start: 2013/10  
Project_Status: Finished  
Project_Authors: Alexandre Fonseca, Anh Thu Vu  

This project was created as an assigment for the Implementation of Distributed Systems and Scientific Writing courses during my semester at KTH.

The aim of this project was to find out just how feasible the distribution of the alignment of genome sequences over several machines is in a world that is still largely dominated by single-machine multiple-core sequence aligners. To that end, we evaluated the performance of 5 different aligners with the same input data, focusing on alignment duration and accuracy. The considered aligners were:

* Centralized (non-distributed)
    * [Bowtie1](http://bowtie-bio.sourceforge.net) - 1.0.0
    * [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/) - 2.1.0
    * [BWA](http://bio-bwa.sourceforge.net) - 0.5.10
* Distributed
    * [Crossbow](http://bowtie-bio.sourceforge.net/crossbow/) - 1.2.1
    * [SEAL](http://biodoop-seal.sourceforge.net/) - 0.3.2

Based on our results, we concluded that distributing the alignment process is feasible. We were able to obtain more than 3x speedup with a relatively small cluster of 5 nodes with a negligible impact in accuracy. We have also noticed that different aligners have different optimization areas with some favouring accuracy while others favour speed. FInally, we have noticed that most of the aligners currently implemented rely on old algorithms and that newer, more sophisticated ones provide good opportunities for further speedup.
