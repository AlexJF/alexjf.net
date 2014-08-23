Title: Anacom
Logo: {static images/logo.png}
Project_Start: 2012/02
Project_Authors: Alexandre Fonseca, Pedro Luz, João Quitério, David Forte, Hugo Almeida, Rui Silva
Project_Version: 1.0
Project_Status: Finished
Gallery:
    {static images/arch.png}||System architecture
    {static images/handlers.png}||Service handlers for security
    {static images/biz1.png}||Byzantine failure handling with state changes and unordered message detection
    {static images/UMLreplication.png}||Replication system UML
    {static images/securityUML.png}||Security system UML
Attachments:
    {static files/anacom.zip}||Project and reports

This project was created as an assigment for the Software Engineering and
Distributed Systems course during my 6th semester at IST.

In this project we were tasked with the creation of a mobile communications
network manager composed of several servers, tolerating one server failure
(crash or byzantine behaviour) even in the presence of big network delays.

<!-- PELICAN_END_SUMMARY -->

The project was split in 4 parts:

* Domain layer design, implementation and testing: Cellphone, Network,
  Communication, etc.
* Service layer design, implementation and testing: SendSMS, SendCall, etc.
* Development of a web interface for the system using GWT and implementation of
  network servers using JAX-WS under JBoss 7 found through a UDDI server.
  Service interface through SOAP.
* Implementation of non-functional requirements for the distributed servers:
  tolerate 1 byzantine or non-byzantine failure and provide adequate security.
  This last part was managed through the Scrum methodology.

Failure tolerance was implemented through a quorum-based active replication
protocol employing a quorum of 4 nodes among the 5 replicas.

The security requirements were that attempts to tamper or replay messages had
to fail to compromise the system. To that end, all messages exchanged between
the server cluster are digitally signed and certified by a Certification
Authority system which we also had to implement. The prevention of replay
attacks was accomplished by introducing a UUID unique to each message and
duplicate detection.
