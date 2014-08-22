Title: Evaluation of NoSQL databases for large-scale decentralized microblogging
Logo: {static images/logo.png}
Project_Start: 2013/01
Project_Authors: Alexandre Fonseca, Anh Thu Vu
Project_Version: 1.0
Project_Status: Finished
Attachments:
    {static files/report.pdf}||Paper
    {static "files/Evaluation of NoSQL databases for microblogging.pdf"}||Presentation for the Decentralized Systems course
    {static "files/A Non-Relational Storage Analysis.pdf"}||Presentation for the Cloud Computing course (compacted and with multi-region data)
    {static files/clc.zip}||Pydloader, results and other files

This project was created as an assigment for the Decentralized Systems and Cloud Computing courses during my 2nd semester at UPC.

In this project, we were asked to do something related to decentralized systems and cloud computing. Having recently had an introduction to NoSQL languages, our group decided to make a comparison between Cassandra and Couchbase in the context of a twitter-like application.

We used 20 AWS nodes: 6 m1.small database nodes and 12 t1.micro workload generating nodes. For the coordination of workloads and result gathering, we created a Python system which we named PyDLoader composed of an interactive management console and a set of slaves that automatically set up and populated the databases on the database nodes and generated workloads in the workload nodes.

Considered in this evaluation:

* Ease of setup and setup time.
* Latencies for the main actions of the application (tweet, userline, timeline).
* Effect of data normalization on the latency.
* Scaling of denormalization.
* Reconfiguration latency (time until cluster stabilizes after a node joins/leaves) and impact on action latency.
* Consistency/Convergence latency (time until all replicas have the same data).
* Replication and crash handling.
* Load balancing.
* System load.
* Disk usage.
* Multi-region setup time, action latency and consistency.
