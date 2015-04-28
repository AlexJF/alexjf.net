Title: Hadoop YARN Installation: The definitive guide
Logo: {static images/elephant_sq.png}
Modified: 2014-06-27
Tags: Hadoop, HDFS, YARN
Description: Installation guide for Hadoop 2.x.x based on YARN with HDFS, YARN 
             and MapReduce configurations for single-node and cluster environments.
Summary: This article guides you in the installation of the new generation
         Hadoop based on YARN. It is based on the most recent version of Hadoop
         at the time of this writing (2.2.0) and includes HDFS, YARN and
         MapReduce configurations for both single-node and cluster
         environments.


[TOC]

<div class='center-text ad' style='margin: 15px'>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- AlexJF - Hadoop Yarn Tutorial -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-7030271622919244"
     data-ad-slot="8008245913"
     data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>

## Introduction
Hadoop is one of the most popular open-source distributed computation frameworks, popularized by the widely used MapReduce computation paradigm. However, recently, Hadoop as been trying to distance itself from a single computation model and provide an abstraction layer over a cluster of machines with which you can easily develop a great variety of fault-tolerant and scalable distributed computation paradigms. In a sense, Hadoop is now trying to become a "kernel" of the distributed cluster, handling the low level details so you don't have to, a kind of Linux for clusters.

Due to this paradigm change in Hadoop, we can identify 2 different Hadoop generations: pre-YARN and post-YARN (2.x). YARN (Yet Another Resource Manager) constitutes a significant improvement over the previous method of handling resources and applications inside Hadoop. To get a better idea of what exactly changed from the previous generation, you can have a look at these presentations by [Spotify](http://www.slideshare.net/AdamKawa/apache-hadoop-yarn-simply-explained) and [Hortonworks](http://www.slideshare.net/hortonworks/apache-hadoop-yarn-enabling-nex). In a nutshell, the main features are:

* Better scaling due to reduced centralization of responsabilities. Should easily support over 10K nodes, 10K jobs and 100K tasks (previous generation started getting into trouble at 4K nodes and 40K tasks).
* More flexibility in resource allocations. You can now easily specify the requirements of each individual container directly in your YARN application, specifying needed RAM, CPU cores and even specific hosts on which the container should be allocated. Previously this was limited to global memory and CPU limits for all containers specified in configuration files.
* More flexibility in computation. Previous Hadoop generations only ran MapReduce jobs. With YARN, Hadoop can run virtually any kind of computation. MapReduce is still possible but is implemented as a backwards-compatible module called MapReducev2 (not enabled by default). Other modules exist such as [Giraph](http://giraph.apache.org/) for graph processing, [Spark](http://spark.incubator.apache.org/) for general computations with intermediate results stored in memory, etc.
* Better failure handling. Previous generations had a single point of failure in the JobTracker losing the entire job queue in such an event. New generation has (or will soon have) recovery of both ApplicationMaster (through a restart by the ResourceManager) and the ResourceManager (through ZooKeeper, YARN-128, YARN-149, YARN-556).
* Wire-compatible protocol. This should guarantee protocol compatibility even between different versions of Hadoop so you no longer have to worry about having to simultaneously update the entire cluster and can do rolling upgrades.

This guide is based on the most recent GA (general access) version of Hadoop (2.2.0 at the time of this writing) although I'll make an effort to keep it up to date with future releases (UPDATE: tested and working up to version 2.6.0). If something doesn't quite work for you, let me know in the comments and I'll try to help. I'll try to keep the instructions distribution agnostic so it applies to a greater audience but this installation is targeted for Linux-based machines. Certain distributions might have different hadoop packages in their repositories although these are usually outdated and have strange structures. Another advantage of the installation I'll be detailing here is that it doesn't require root to run.

## Single Node Installation
In this section, we'll cover single node installation. If you just want to setup an Hadoop installation for testing or to play with, this is probably enough. If you want to install Hadoop on a cluster, you should also start by following this section on one of the nodes in the cluster to make sure you got all the dependencies right and then go over the steps in the Cluster Installation to configure that installation for cluster operation.

We can think of Hadoop as 2 different components: HDFS, a distributed filesystem; and YARN, the resource manager which takes care of allocating containers where jobs can run using the data stored in HDFS. We'll cover the configuration of each of these components separately later on. But first, lets start with the basics:

### Install Hadoop
Installing Hadoop is as easy as going to the Hadoop website, downloading the [latest stable version](http://apache.mirrors.spacedump.net/hadoop/common/stable/) and unpacking it to a directory of your choice. In this case I'll just use `~/Programs` so hadoop will be installed in `~/Programs/hadoop-2.2.0`:

```bash
mkdir -p ~/Programs # Feel free to change this to the dir where you want hadoop to reside
cd ~/Programs 
wget http://apache.mirrors.spacedump.net/hadoop/common/stable/hadoop-2.2.0.tar.gz
tar xvf hadoop-2.2.0.tar.gz --gzip
rm hadoop-2.2.0.tar.gz # We no longer need the tar
```

Also, you should install a java virtual machine (JVM). I usually go with OpenJDK's JRE 7 but any other should do. And that was it! Easy right? Now lets just set up some environmental values needed by some scripts inside Hadoop and also to facilitate references to the installed location. The following lines should be added to either your `~/.bashrc` (if you use Bash); `~/.zshrc` (if you use Zsh); `~/.profile` (I know this works with Bash, not sure about others); or whatever file your usual terminal shell uses to setup environment variables and alias.

```bash
export HADOOP_PREFIX="/home/alex/Programs/hadoop-2.2.0" # Change this to where you unpacked hadoop to.
```

That export alone is sufficient for running simple YARN or MapReduce applications. Other applications building on top of Hadoop might expect a plethora of other environment variables. Here are some of the most usual in case those apps complain they are missing:

```bash
export HADOOP_HOME=$HADOOP_PREFIX
export HADOOP_COMMON_HOME=$HADOOP_PREFIX
export HADOOP_CONF_DIR=$HADOOP_PREFIX/etc/hadoop
export HADOOP_HDFS_HOME=$HADOOP_PREFIX
export HADOOP_MAPRED_HOME=$HADOOP_PREFIX
export HADOOP_YARN_HOME=$HADOOP_PREFIX
```

Now lets move on to configuring the 2 main components: HDFS and YARN.

### HDFS Configuration
HDFS is the distributed file system used by Hadoop to store data in the cluster, capable of hosting very very (very) large files, splitting them over the nodes of the cluster. Theoretically, you don't need to have it running and files could instead be stored elsewhere like S3 or even the local file system (if using a purely local Hadoop installation). However, some applications require interactions with HDFS so you may have to set it up sooner or later if you're using third party modules. HDFS is composed of a NameNode which holds all the metadata regarding the stored files, and DataNodes (one per node in the cluster) which hold the actual data.

The main HDFS configuration file is located at `$HADOOP_PREFIX/etc/hadoop/hdfs-site.xml`. If you've been following since the beginning, this file should be empty so it will use the default configurations outlined in [this page](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml). For a single-node installation of HDFS you'll want to change `hdfs-site.xml` to have, at the very least, the following:

```xml
<configuration>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/alex/Programs/hadoop-2.2.0/hdfs/datanode</value>
        <description>Comma separated list of paths on the local filesystem of a DataNode where it should store its blocks.</description>
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/alex/Programs/hadoop-2.2.0/hdfs/namenode</value>
        <description>Path on the local filesystem where the NameNode stores the namespace and transaction logs persistently.</description>
    </property>
</configuration>
```

Make sure to replace `/home/alex/Programs/hadoop-2.2.0` with whatever you set `$HADOOP_PREFIX` to. In addition, add the following to `$HADOOP_PREFIX/etc/hadoop/core-site.xml` to let the Hadoop modules know where the HDFS NameNode is located.

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost/</value>
        <description>NameNode URI</description>
    </property>
</configuration>
```

### YARN Configuration
YARN is the component responsible for allocating containers to run tasks, coordinating the execution of said tasks, restart them in case of failure, among other housekeeping. Just like HDFS, it also has 2 main components: a ResourceManager which keeps track of the cluster resources and NodeManagers in each of the nodes which communicates with the ResourceManager and sets up containers for execution of tasks.

To configure YARN, the relevant file is `$HADOOP_PREFIX/etc/hadoop/yarn-site.xml`. The file should currently be empty which means it's using the default configurations you can find [here](http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-common/yarn-default.xml). For a single-node installation of YARN you'll want to add the following to that file:

```xml
<configuration>
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>128</value>
        <description>Minimum limit of memory to allocate to each container request at the Resource Manager.</description>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>2048</value>
        <description>Maximum limit of memory to allocate to each container request at the Resource Manager.</description>
    </property>
    <property>
        <name>yarn.scheduler.minimum-allocation-vcores</name>
        <value>1</value>
        <description>The minimum allocation for every container request at the RM, in terms of virtual CPU cores. Requests lower than this won't take effect, and the specified value will get allocated the minimum.</description>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-vcores</name>
        <value>2</value>
        <description>The maximum allocation for every container request at the RM, in terms of virtual CPU cores. Requests higher than this won't take effect, and will get capped to this value.</description>
    </property>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>4096</value>
        <description>Physical memory, in MB, to be made available to running containers</description>
    </property>
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
        <description>Number of CPU cores that can be allocated for containers.</description>
    </property>
</configuration>
```

As in the HDFS case, whenever you see `/home/alex/Programs/hadoop-2.2.0`, you'll want to replace it by the content of your $HADOOP_PREFIX variable. The values above were the ones I used on my 6GB laptop with 4 virtual cores. In a nutshell, I'm saying that of those resources, I want Hadoop to use at most 4GB and 4 virtual cores and that each container can have between 128MB and 2GB of memory and between 1 and 2 virtual cores. With these settings, I can run a minimum of 2 containers with maximum resources at a time: 2 containers with 2GB and 2 virtual cores. You should adapt these to your specific case.

### Starting
Now that we've finished configuring everything, it's time to setup the folders and start the daemons:

```bash
## Start HDFS daemons
# Format the namenode directory (DO THIS ONLY ONCE, THE FIRST TIME)
$HADOOP_PREFIX/bin/hdfs namenode -format
# Start the namenode daemon
$HADOOP_PREFIX/sbin/hadoop-daemon.sh start namenode
# Start the datanode daemon
$HADOOP_PREFIX/sbin/hadoop-daemon.sh start datanode

## Start YARN daemons
# Start the resourcemanager daemon
$HADOOP_PREFIX/sbin/yarn-daemon.sh start resourcemanager
# Start the nodemanager daemon
$HADOOP_PREFIX/sbin/yarn-daemon.sh start nodemanager
```

Hopefully, everything should be running. Use the command `jps` to see if all daemons are launched. If one is missing, check `$HADOOP_PREFIX/logs/<daemon with problems>.log` for any errors. 

### Testing {#single-node-test}
To test if everything is working ok, lets run one of the example applications shipped with Hadoop called DistributedShell. This application spawns a specified number of containers and runs a shell command in each of them. Lets run DistributedShell with the 'date' command which outputs the current time:

```bash
# Run Distributed shell with 2 containers and executing the script `date`.
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/share/hadoop/yarn/hadoop-yarn-applications-distributedshell-2.2.0.jar org.apache.hadoop.yarn.applications.distributedshell.Client --jar $HADOOP_PREFIX/share/hadoop/yarn/hadoop-yarn-applications-distributedshell-2.2.0.jar --shell_command date --num_containers 2 --master_memory 1024
```

With this command we are telling hadoop to run the `Client` class in the `hadoop-yarn-applications-distributedshell-2.2.0.jar`, passing it the jar containing the definition of the ApplicationMaster (the same jar), the shell command to run in each of the hosts (`date`), the number of containers to spawn (2) and the memory used by the ApplicationMaster (1024MB). The value of 1024 was set empirically by trying to run the program several times until it stopped failing due to the ApplicationMaster using more memory than that which had been allocated to it. You can check the entire set of parameters you can pass to DistributedShell by using the same command without any arguments:

```bash
# Check the parameters for the DistributedShell client.
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/share/hadoop/yarn/hadoop-yarn-applications-distributedshell-2.2.0.jar org.apache.hadoop.yarn.applications.distributedshell.Client
```

Hopefully, the execution of the first command resulted in a `INFO distributedshell.Client: Application completed successfully`. Find the application ID by checking the output of the command for a string similar to this: `application_1385919023711_0001`. Now, to check the outputs of the containers, run the following command:

```bash
# Substitute <APPLICATION ID> for the one you found on the output of the command
grep "" $HADOOP_PREFIX/logs/userlogs/<APPLICATION ID>/**/stdout
```

If you have correctly followed this guide and if the gods are favourable towards you, you should see time strings with the current time, one for each container. If that's the case, good job! You've just setup a single-node installation of Hadoop YARN! If your objective is to setup a whole cluster, carry on to the next section. Otherwise, and if your objective is to run MapReduce jobs, jump to the [last section](#mrconfig) because we need some extra configuration to allow the running of MapReduce jobs over YARN.

## Cluster Installation
**NOTE:** This is a continuation of the configuration steps for single-node executions, so make sure to read that first.

Having configured Hadoop in a single node, configuring it in an entire cluster is not that hard. Basically, you just have to install Hadoop on all the nodes and use the same configuration (at least the endpoints of each of the services) on all of them. However, this time, you won't be running all the daemons in all the nodes. Per cluster you'll have a single ResourceManager and one (or more if using secondary/backups) NameNode. DataNode and NodeManager daemons should be run in all the nodes if you have a small cluster and/or a small number of jobs. With a bigger cluster or a bigger number of jobs you might want to have a dedicated node for both the ResourceManager and NameNode to reduce contention. All the machines with a DataNode and NodeManager are called slaves (a slave can also be a master if you run the other daemons on the same node as we did on the single node setup). 

### HDFS Configuration
In the HDFS configuration, the only thing you are really required to change is the `fs.defaultFS` parameter in `$HADOOP_PREFIX/etc/hadoop/core-site.xml`. This should point to the endpoint of the node running the NameNode daemon (if you're running it in a non-default port, add a `:<port number>` before the last /:

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://namenode.alexjf.net/</value>
        <description>NameNode URI</description>
    </property>
</configuration>
```

### YARN Configuration
For the YARN configuration, you can customize the entries we saw on the single-node installation (memory and CPU) to the resources of each node. But you'll then have to add the hostname of the ResourceManager to all the `yarn-site.xml`. If you want to customize the ports, check the [default configuration](http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-common/yarn-default.xml) for the parameters you need to change.

```xml
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>resourcemanager.alexjf.net</value>
        <description>The hostname of the RM.</description>
    </property>
</configuration>
```

### Starting

#### Manually
Once all nodes have the same endpoint configuration, you can start the daemons in all of them:

```bash
## Start HDFS daemons
# Format the namenode directory (DO THIS ONLY ONCE, THE FIRST TIME)
# ONLY ON THE NAMENODE NODE
$HADOOP_PREFIX/bin/hdfs namenode -format
# Start the namenode daemon
# ONLY ON THE NAMENODE NODE
$HADOOP_PREFIX/sbin/hadoop-daemon.sh start namenode
# Start the datanode daemon
# ON ALL SLAVES
$HADOOP_PREFIX/sbin/hadoop-daemon.sh start datanode

## Start YARN daemons
# Start the resourcemanager daemon
# ONLY ON THE RESOURCEMANAGER NODE
$HADOOP_PREFIX/sbin/yarn-daemon.sh start resourcemanager
# Start the nodemanager daemon
# ON ALL SLAVES
$HADOOP_PREFIX/sbin/yarn-daemon.sh start nodemanager
```

#### Hadoop Scripts
Since manually launching the daemons in every node is quite bothersome, Hadoop ships with a few scripts that aim to help you with this task. They, however, assume that the node where you run the ResourceManager has SSH access to all of the nodes in the cluster (including itself) and that you specify the hostnames of all the slaves in the `$HADOOP_PREFIX/etc/hadoop/slaves` file:

```
slave1.alexjf.net
slave2.alexjf.net
slave3.alexjf.net
slave4.alexjf.net
slave5.alexjf.net
```

To launch the nodes you just have to SSH into the ResourceManager node and run the following:

```bash
# Start all HDFS services cluster-wide
$HADOOP_PREFIX/sbin/start-dfs.sh
# Start all YARN services clluster-wide
$HADOOP_PREFIX/sbin/start-yarn.sh
```

NOTE: If your installed Java package doesn't do it by default, the above scripts can complain about an incorrect `$JAVA_HOME` environment variable. To fix this, point it to the directory where Java was installed. In my case, it is: `/usr/lib/jvm/java-7-openjdk`.

#### Other deployment scripts
For greater flexibility and for automating the downloading and extracting of the Hadoop package or even the allocation of computation nodes via, for example, EC2 or Azure, you might want to use custom deployment scripts and frameworks. Some of the options here would be [Fabric](http://fabfile.org), [Vagrant](http://www.vagrantup.com/), [Puppet](http://puppetlabs.com/), [Chef](http://www.opscode.com/chef/), among many others. Since I usually only setup Hadoop clusters on "normal" dedicated servers, I'm quite partial to the simplicity of Fabric. I have created a script for deploying Hadoop on my clusters which I'll share with you in the next paragraph. This script assumes the machine where you run it (it doesn't have to belong to the cluster, might be your simple laptop) has SSH access to all the cluster machines and that you have managed to [install Fabric](http://docs.fabfile.org/en/1.8/#installation) (which requires Python 2 and Paramiko) on the machine where you want to run it (don't need to install it on any other). 

Get the script from my [Github repo](https://github.com/AlexJF/fabric-scripts/tree/master/hadoop-yarn). To use it, just edit the top sections of the script to setup your cluster configuration and run the following in this order from the folder containing the `fabfile.py`:

```bash
# Install dependencies (like Java)
fab installDependencies
# Install Hadoop
fab install
# Config Hadoop
fab config
# Setup environment variables
fab setupEnvironment
# Format HDFS NameNode (THIS WILL DELETE EVERYTHING IN YOUR HDFS FS)
fab formatHdfs
# Start daemons
fab start
# Stop daemons
fab stop
```

Assuming you configured everything correctly that should have worked ok. If not, drop me a comment and I'll try to help you! 

### Troubleshooting

#### Bind Exception
If one or more of hadoop's components don't start complaining about not being able to bind to an address or port already in use check the following: 

* No other application is running on that port `fuser -v -n tcp <port number>`. If it is, kill it or use a different port (change the respective `*-site.xml`).
* The hostname of your node should point to its internal address. This is configured through `/etc/hosts`. For example, in my `resourcemanager.alexjf.net` node, the `/etc/hosts` file contains something like `192.168.1.1 resourcemanager.alexjf.net`. To find out the IP address you need to put there use `ifconfig eth0`. 
* Nodes are accessible from one another using the URLs you defined in the configuration. If this is not the case, you should unblock ports and/or add extra mappings to `/etc/hosts`.

My Fabric script described above has a special command to map the public URLs used in the configuration to cluster-private IPs directly to the hosts file of every node: `fab setupHosts`. This command also writes these private IPs to a file in the home directory of the ResourceManager host.

### Testing
For testing the cluster installation, follow the same steps as in the [testing for the single-node installation](#single-node-test). However, try to increase the number of containers to try and have tasks in every one of your slaves. You may call the DistributedShell client from any of the nodes in the cluster (or from your own laptop if you have hadoop installed and pointing to the correct endpoints). Alternatively, using my Fabric script, just run:

```bash
# Execute the DistributedShell app with the 'date' command.
fab test
```

## MapReduce 
Whereas in previous versions of Hadoop MapReduce was the only computational model you could use, with YARN this is no longer the case. Thus, up until now, I've kept the entire guide independent from MapReduce executions. If you just want to install Hadoop to run other YARN-enabled applications like Giraph or Spark, the previous sections should have enabled you to setup everything regarding YARN. If, however, your focus is indeed on running MapReduce jobs, then we need to configure MapReducev2, the YARN-enabled MapReduce that ships with the new generations of Hadoop. 

### Configuration {#mrconfig} 
Fortunately, this is not too difficult. We just need to setup some reasonable defaults for the memory and CPU requirements in `mapred-site.xml`to match those we defined for the YARN containers previously:

```xml
<configuration>
    <property>
        <name>yarn.app.mapreduce.am.resource.mb</name>
        <value>1024</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.command-opts</name>
        <value>-Xmx768m</value>
    </property>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
        <description>Execution framework.</description>
    </property>
    <property>
        <name>mapreduce.map.cpu.vcores</name>
        <value>1</value>
        <description>The number of virtual cores required for each map task.</description>
    </property>
    <property>
        <name>mapreduce.reduce.cpu.vcores</name>
        <value>1</value>
        <description>The number of virtual cores required for each map task.</description>
    </property>
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>1024</value>
        <description>Larger resource limit for maps.</description>
    </property>
    <property>
        <name>mapreduce.map.java.opts</name>
        <value>-Xmx768m</value>
        <description>Heap-size for child jvms of maps.</description>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>1024</value>
        <description>Larger resource limit for reduces.</description>
    </property>
    <property>
        <name>mapreduce.reduce.java.opts</name>
        <value>-Xmx768m</value>
        <description>Heap-size for child jvms of reduces.</description>
    </property>
    <property>
        <name>mapreduce.jobtracker.address</name>
        <value>jobtracker.alexjf.net:8021</value>
    </property>
</configuration>
```

The `java.opts` properties specify some extra arguments for launching the Java Virtual Machine for the mappers, reducers and application master. As a rule of thumb, you should limit the heap-size to about 75% of the total memory available to ensure things run more smoothly. With this configuration, I can theoretically have up to 4 mappers/reducers running simultaneously in 4 1GB containers. In practice, the MapReduce application master will use a 1GB container so the actual number of concurrent mappers and reducers will be limited to 3. You can play around with the memory limits but it might require some experimentation to find the best ones. Too low and you'll get out of memory exceptions, too high and you'll have very few mappers/reducers or the ApplicationMaster will consume a great portion of the resources unnecessarily. Also, note that the mapper/reducer memory/cpu settings above are just defaults in case the actual MapReduce applications don't define their own requirements. An application can define requirements much bigger than these in which case it will not be able to run in your cluster.

The jobtracker configuration specifies which node of the cluster should be responsible for being the JobTracker. If you're doing a single-node setup, you can leave it at the default value of "local".

In addition to the configuration in `mapred-site.xml`, we also need to setup a prerequisite for MapReduce in `yarn-site.xml`: the mapreduce_shuffle auxiliary service. Just add the following to the end of `yarn-site.xml`:

```xml
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
        <description>shuffle service that needs to be set for Map Reduce to run </description>
    </property>
```

With this configuration, you should already be able to run MapReduce jobs.

### Starting
MapReduce jobs don't need any extra daemon running other than the ones already launched for pure YARN applications. JobTrackers and TaskTrackers will be launched automatically by the MapReduce Application Master.

### Testing
To test our MapReduce configuration, lets run one of the packaged MapReduce examples: RandomWriter. In one of the nodes in your cluster, run the following on any of the nodes of the cluster:

```bash
# Execute randomwriter example
$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.2.0.jar randomwriter out
```

Once again, if you are using my Fabric scripts, there's a function for that:

```bash
fab testMapReduce
```

### Streaming MapReduce
The RandomWriter program we ran in the previous section is an example of a MapReduce application coded in Java and packaged into a jar. This is the basic way to run MapReduce jobs. Another popular way to run these jobs in previous versions was through MapReduce Streaming applications. In these executions of MapReduce, instead of providing a jar with the compiled Java application code, you provide mapper and a reducer scripts written in any language which read from the standard input and output to the standard output.

Fortunately, this is still possible with new generation Hadoop. Lets take the whole too popular Python wordcount mapreduce example:

```python
#!/usr/bin/env python
# mapper.py file

import sys

for line in sys.stdin:
    line = line.strip() # Remove whitespace from beginning and end
    words = line.split() # Split content by whitespace (get words)
    for word in words:
        print('%s\t%s' % (word, 1)) # Print '<word> 1' registering its occurence
```

```python
#!/usr/bin/env python
# reducer.py file

from operator import itemgetter
import sys

currentWord = None
currentCount = 0

for line in sys.stdin:
    line = line.strip()

    # Get elements of pair created by the mapper
    word, count = line.split()

    # Convert count to an integer
    try:
        count = int(count)
    except ValueError:
        continue

    # Hadoop passes pairs ordered by key (first value), so
    # we can be sure that all pairs with the same key will
    # sent sequentially. When we detect a different one, we
    # won't see that word again.
    if currentWord != word:
        if currentWord is not None:
            print('%s\t%d' % (currentWord, currentCount))
        currentWord = word
        currentCount = 0

    currentCount += count

# Output last word group if needed
if currentCount > 0:
    print('%s\t%d' % (currentWord, currentCount))
```

```bash
# Send mapper.py and reducer.py to cluster and use them as mapper and reducer for a MapReduce job
$HADOOP_PREFIX/bin/hadoop  jar $HADOOP_PREFIX/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar  \
    -input myInputDir \
    -output myOutputDir \
    -mapper mapper.py \
    -reducer reducer.py \
    -file mapper.py \
    -file reducer.py
```

## Extra/Advanced stuff

### Adding Hadoop binaries to the path
In case you find that using the hadoop binaries by always specifying the `$HADOOP_PREFIX/bin` prefix is too troublesome, you can add this directory to your path. To do so, just go to your shell's configuration file (`.bashrc` for bash, `.zshrc` for zsh) and add the following:

```bash
export PATH=$HADOOP_PREFIX/bin:$PATH
```

After doing this and opening a new shell (or sourcing the changed configuration file), you should be able to directly use hadoop commands:

```bash
hadoop version
hdfs dfs -ls /
...
```

### Web Interface
To monitor your cluster and your jobs, you can also check the web interfaces of the Hadoop components instead of using the command line for that. This web interface is available at the endpoint of your ResourceManager node at the webapp port (by default 8088). In a single-node setup you could access it with [localhost:8088](localhost:8088). In the cluster setup with `resourcemanager.alexjf.net:8088`. You'll be greeted with a web page that looks like the following:

<div class="center-text">
<a href="{static images/snapshot1.png}" title="Hadoop Web Interface" class="image-box">
<img src="{static images/snapshot1.png thumb=220x165}" alt="Hadoop Web Interface" class="blogpost-image image-medium" /></a>
</div>

### Log Aggregation {#log-aggregation}
By default, Hadoop stores the logs of each container in the node where that container was hosted. While this is irrelevant if you're just testing some Hadoop executions in a single-node environment (as all the logs will be in your machine anyway), with a cluster of nodes, keeping track of the logs can become quite a bother. In addition, since logs are kept on the normal filesystem, you may run into storage problems if you keep logs for a long time or have heterogeneous storage capabilities.

Log aggregation is a new feature that allows Hadoop to store the logs of each application in a central directory in HDFS. To activate it, just add the following to `yarn-site.xml` and restart the Hadoop services:

```xml
    <property>
        <description>Whether to enable log aggregation</description>
        <name>yarn.log-aggregation-enable</name>
        <value>true</value>
    </property>
```

By adding this option, you're telling Hadoop to move the application logs to `hdfs:///logs/userlogs/<your user>/<app id>`. You can change this path and other options related to log aggregation by specifying some other properties mentioned in the [default yarn-site.xml](http://hadoop.apache.org/docs/current2/hadoop-yarn/hadoop-yarn-common/yarn-default.xml) (just do a search for `log.aggregation`).

However, these aggregated logs are [not stored in a human readable format](https://issues.apache.org/jira/browse/YARN-1440) so you can't just `cat` their contents. Fortunately, Hadoop developers have included several handy command line tools for reading them:

```bash
# Read logs from any YARN application
$HADOOP_HOME/bin/yarn logs -applicationId <applicationId>

# Read logs from MapReduce jobs
$HADOOP_HOME/bin/mapred job -logs <jobId>

# Read it in a scrollable window with search (type '/' followed by your query).
$HADOOP_HOME/bin/yarn logs -applicationId <applicationId> | less

# Or just save it to a file and use your favourite editor
$HADOOP_HOME/bin/yarn logs -applicationId <applicationId> > log.txt
```

You can also access these logs via a web app for MapReduce jobs by using the JobHistory daemon. This daemon can be started/stopped by running the following:

```bash
# Start JobHistory daemon
$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh start historyserver
# Stop JobHistory daemon
$HADOOP_PREFIX/sbin/mr-jobhistory-daemon.sh stop historyserver
```

My Fabric script includes an optional variable for setting the node where to launch this daemon so it is automatically started/stopped when you run `fab start` or `fab stop`.

Unfortunately, a generic history daemon for universal web access to aggregated logs does not exist yet. However, as you can see by checking [YARN-321](https://issues.apache.org/jira/browse/YARN-321), there's considerable work being done in this area. When this gets introduced I'll update this section.

### S3 Integration

HDFS is able to read and write data from/to [S3](http://aws.amazon.com/s3/) buckets. To achieve this, `core-site.xml` has to be changed to include details about the [AWS Access Key](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html):

```xml
    <property>
        <name>fs.s3n.awsAccessKeyId</name>
        <value>YOUR_KEY_ID</value>
    </property>
    <property>
        <name>fs.s3n.awsSecretAccessKey</name>
        <value>YOUR_SECRET_KEY</value>
    </property>
```

You can now read/write to a bucket using the following commands (they apply to both files and folders):

```bash
# Uploading a local file to a S3 bucket
hdfs dfs -put example.file s3n://bucketname/somefolder
# Uploading a HDFS file to a S3 bucket
hdfs dfs -cp example.file s3n://bucketname/somefolder
# Downloading a file in S3 to local FS
hdfs dfs -get s3n://bucketname/somefolder/somefile
# Downloading a file in S3 to HDFS
hdfs dfs -cp s3n://bucketname/somefolder/somefile /hdfs/path/somefile
```

In addition, you can also use the s3n URL directly as the input for your jobs without having to do an intermediate copy.

An alternative S3 filesystem exists with a s3:// URI scheme. However, this is reserved for accessing HDFS-formatted S3 buckets. [This stackoverflow question](http://stackoverflow.com/questions/10569455/difference-between-amazon-s3-and-s3n-in-hadoop) gives a good overview of the differences between the 2 filesystems.

### EC2 deployment with Fabric script

Following these instructions, you should easily be able to do a complete Hadoop deployment over EC2. Just launch the instances and configure them as a normal cluster. However, if you're using EC2, chances are the cluster you're setting up will be temporary and you'll have to redo the entire sequence of steps each time you want to setup a new one. To tackle this problem, my [Fabric script](https://github.com/AlexJF/fabric-scripts/tree/master/hadoop-yarn) now includes automatic EC2 instance-finding and bootstrapping. To make use of this function, download the entire contents of the script folder and modify the entries at the top of `fabfile.py` to reflect your preferences and configuration (make sure you activate EC2 deployment by setting the option with the same name to True and to add your AWS_ACCESSKEY_* values).

Now, when launching your instances, specify a common tag with `Cluster` as key and whatever the value of `EC2_CLUSTER_NAME` is set to in `fabfile.py`. All instances with a `Cluster` tag matching the value in the configuration will be automatically discovered and included as slaves. The resourcemanager, namenode, jobhistory and jobtracker nodes will be automatically chosen among these unless you specifically choose this assignment by adding the following optional tag keys (with any value) to any of the cluster instances:

* `resourcemanager`
* `namenode`
* `jobhistory`
* `jobtracker`

You can check if the instance assignment looks correct by running the following command in the folder containing `fabfile.py`:

```bash
# Check if host assignment is correct
fab debugHosts
```

If everything looks ok, you can bootstrap and test the entire Hadoop cluster by issueing:

```bash
# Bootstrap all cluster nodes in parallel (if you detect any problems, remove -P for serial execution)
fab -P bootstrap
# Wait a minute or two for the system to stabilize
fab test
```

### Native hadoop library and 64-bit JVMs

Hadoop ships with a precompiled 32-bit native library [used for efficient compression/decompression](http://hadoop.apache.org/docs/r2.4.0/hadoop-project-dist/hadoop-common/NativeLibraries.html#Components). If you try to run Hadoop on a 64-bit JVM with this precompiled library, you might be greeted with the following error:

```
OpenJDK 64-Bit Server VM warning: You have loaded library /home/hadoop/hadoop-2.2.0/lib/native/libhadoop.so.1.0.0 which might have disabled stack guard. The VM will try to fix the stack guard now. It's highly recommended that you fix the library with 'execstack -c <libfile>', or link it with '-z noexecstack'.
```

I have never noticed anything breaking by not using the native libraries but, if you rely a lot on compression, the Java implementations used as a fallback will surely be a lot less performant than the native ones.

Now, despite what the error message tells you, executing the `execstack` command won't fix anything (at least it never did for me). The right way to fix this issue is to do one of the following:

* Run Hadoop on a 32 bit JVM.
* Recompile the native libary under a 64 bit environment - [Here](http://hadoop.apache.org/docs/r2.6.0/hadoop-project-dist/hadoop-common/NativeLibraries.html#Build) you can find the official instructions, and [here](http://blog.woopi.org/wordpress/?p=201) you can find unofficial instructions for Debian-like systems and a prepackaged hadoop for 64bits.

(NOTE: Thank you Chris L. for suggesting this extra section).


## Conclusion
If you've reached this section and everything's working ok, congratulations! You've just setup a Hadoop Yarn cluster (or single-node setup). This guide has covered the basic aspects of Hadoop. Some other things you might want to consider are authentication, connection with Amazon S3, etc. I'm open to suggestions for other guides and critiques so make sure to give your feedback using the comment form below.

Hope you've enjoyed reading this :)

**Changelog:**

* 2015-04-24 - Added a section regarding native library and 64 bits incompatibility.
* 2014-06-27 - Added S3 and EC2 deployment sections. Updated Fabric scripts. 
* 2014-03-17
    * Added a section explaining how to add hadoop binaries to the execution path.
* 2014-01-27
    * Fixed wrong if condition in example Python streaming program.
    * Added log aggregation section
    * Added `mapreduce.jobtracker.address` to the MapReduce configuration section.
    * Updated the Fabric scripts for server-side Python 2.6 compatibility, more adaptibility and bugfixing.
* 2014-01-07 - Fixed typos and duplicate command in resourcemanager/nodemanager startup with Hadoop scripts.

**Donate:**

If you found this useful and saved you time, consider buying me a beer :) 
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----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-----END PKCS7-----
">
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">
</form>

<div class='center-text ad' style='margin: 15px'>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- AlexJF - Hadoop Yarn Tutorial -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-7030271622919244"
     data-ad-slot="8008245913"
     data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>
