### GeoMesa ON OpenStack VM Ubuntu 16.04
by Charles Thao. Updated August 1st, 2017

This is an installation guide for installing GeoMesa/Accumulo on Openstack VM
### Create an OpenStack Instance

### Environment Setup
1. OS update
```
$ apt-get update
```
2. Install SSH
```
$ apt-get install ssh rsync
```
3. Install OpenJDK Java
```
$ sudo apt-get install openjdk-8-jdk
```

4(optional). If your system constantly prompts "Unresolved Host", do the following
```
$ sudo vim /etc/hosts
```

add the following line to the top of the file
```
127.0.0.1 [computer-name]
```
with [computer-name] being your VM's name
### Enable passwordless SSH
1. Activate ssh agent
```
$ eval `ssh-agent -s`
```
2.
```
$ ssh-keygen -P ''
```
When prompted for directory, press enter to created a default key at ~/.ssh/id_rsa

```
$ chmod 700 ~/.ssh/id_rsa
$ ssh-add ~/.ssh/id_rsa
$ ssh-add -l
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 
```

Test ssh
```
ssh localhost
```
### Installation
1. Create Downloads directory
```
$ cd ~/
$ mkdir Downloads
```
2.Download and unpack the binary distributions of Hadoop, Zookeeper and Accumulo
```
$ cd ~/Downloads
$ wget https://archive.apache.org/dist/hadoop/core/hadoop-2.5.2/hadoop-2.5.2.tar.gz
$ wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.4.9/zookeeper-3.4.9.tar.gz
$ wget https://archive.apache.org/dist/accumulo/1.7.2/accumulo-1.7.2-bin.tar.gz
$ tar -xvzf ~/Downloads/accumulo-1.7.2-bin.tar.gz
$ tar -xvzf ~/Downloads/zookeeper-3.4.9.tar.gz
$ tar -xvzf ~/Downloads/hadoop-2.5.2.tar.gz 
```

3. Install the packages
```
$ sudo cp -r accumulo-1.7.2/. /usr/local/accumulo
$ sudo cp -r hadoop-2.5.2/. /usr/local/hadoop
$ sudo cp -r zookeeper-3.4.9/. /usr/local/zookeeper
```
4. Edit ~/.bashrc
```
$ vim ~/.bashrc
```
Add these lines to the file:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
export ACCUMULO_HOME=/usr/local/accumulo
export HADOOP_HOME=/usr/local/hadoop
export ZOOKEEPER_HOME=/usr/local/zookeeper
export PATH=$PATH:/usr/local/hadoop/bin/
export PATH=$PATH:/usr/local/hadoop/sbin/
export PATH=$PATH:/usr/local/accumulo/bin/
export PATH=$PATH:/usr/local/zookeeper/bin/
``` 

On the terminal, source from .bashrc

```
$ . ~/.bashrc
```

### Configure Hadoop HDFS

1. Edit core-site.xml
```
$ sudo vim /usr/local/hadoop/etc/hadoop/core-site.xml 
```
Add this 
```
<property>
   <name>fs.defaultFS</name>
   <value>hdfs://localhost:9000</value>
</property>
```
2. Edit hdfs-site.xml 
```
$ sudo vim /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```

Make sure it looks like this  

```
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.name.dir</name>
        <value>hdfs_storage/name</value>
    </property>
    <property>
        <name>dfs.data.dir</name>
        <value>hdfs_storage/data</value>
    </property>
    <property>
        <name>dfs.support.append</name>
        <value>true</value>
    </property>
    <property>
        <name>dfs.datanode.synconclose</name>
        <value>true</value>
    </property>

```
3. Configure MapReduce
```
$ sudo cp /usr/local/hadoop/etc/hadoop/mapred-site.xml.template /usr/local/hadoop/etc/hadoop/mapred-site.xml
```
add this to the xml:
```
<property>
         <name>mapred.job.tracker</name>
         <value>localhost:9001</value>
</property>
```
4. This step is optional, however sometimes Hadoop NameNode will not be correctly configured without this

Create /hdfs_storage/name
```
$ cd /usr/local/hadoop/
$ sudo mkdir hdfs_storage
$ cd hdfs_storage
$ sudo mkdir name
$ sudo mkdir data
```
5. Configure hadoop environment:
```
$ sudo vim /usr/local/hadoop/etc/hadoop/hadoop-env.sh  
```
Find $JAVA_HOME and edit
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
```
6. 
Initialize storage
```
$ hdfs namenode -format
```
7. Run Hadoop
```
$ start-dfs.sh
```
8. Test
```
$ jps
```
You should get the similar output. If Namenode isn't there, then there must be an error when in "hdfs namenode -format":
```
21097 SecondaryNameNode
20772 NameNode
14036 Jps
20917 DataNode
```
If NameNode isn't showing up, doing the following could help:
```
$ cd $HADOOP_HOME
$ rm -r hdfs_storage/
$ stop-all.sh
$ hadoop namenode -format
$ start-dfs.sh
```

On Horizon, add a rule in your security group that allows access to port 50070(hadoop) and 50095 (accumulo)
On your browser, go to http://[your-serverIP]:50070 to make sure everything is up and running

### Configure ZooKeeper
```
$ cd $ZOOKEEPER_HOME/conf
```

Copy the example conf to zoo.cfg
```
$ sudo cp zoo_sample.cfg zoo.cfg
```
Open zoo.cfg in vim and add this to datadir
```
$ /usr/local/zookeeper-3.4.9/datadir
```
Start zookeeper
```
$ zkServer.sh start
```

### Configure Accumulo


1. Make Accumulo available to the Internet. The default setting only allows access from local network.
```
$ sudo vim /usr/local/accumulo/conf/accumulo-env.sh
```

Uncomment export ACCUMULO_MONITOR_BIND_ALL="true"

2. Build Accumulo's native library
```
$ sudo apt-get install make
$ sudo apt-get install g++
$ sudo apt-get install gcc
$ build_native_library.sh
```

3.
```
$ sudo $ACCUMULO_HOME/bin/bootstrap_config.sh 
```
Input the desired configurations
4. Set HDFS location and other configurations in Accumulo
```
$ vim conf/accumulo-site.xml 
```
Add this to value of instance.volumes: 

hdfs://localhost:9000/accumulo

Some sample settings:

  <property>
    <name>tserver.memory.maps.max</name>
    <value>512M</value>
  </property>

  <property>
    <name>tserver.memory.maps.native.enabled</name>
    <value>false</value>
  </property>

  <property>
    <name>tserver.cache.data.size</name>
    <value>30M</value>
  </property>

  <property>
    <name>tserver.cache.index.size</name>
    <value>80M</value>
  </property>

Also, you should change trace.token.property.password and instance.secret

5. Start Accumulo:

```
$ accumulo init
```
It will ask for an instance name and password, make sure this matches instance.secret
```
$ $ACCUMULO_HOME/bin/start-all
```

Lastly, try if accumulo shell works
```
$ accumulo shell -u root
```
It will prompt for password, which should match trace.token.property.password
You could go to http://[your_server_IP]:50095 to see if Accumulo is up and running

### GeoMesa Installation

Download GeoMesa/Accumulo binary distribution on geomesa.org

```
$ cd ~/Downloads/
$ wget https://repo.locationtech.org/content/repositories/geomesa-releases/org/locationtech/geomesa/geomesa-accumulo-dist_2.11/1.3.2/geomesa-accumulo-dist_2.11-1.3.2-bin.tar.gz
$ tar -xvzf ~/Downloads/geomesa-accumulo-dist_2.11-1.3.2-bin.tar.gz
$ sudo mv -r geomesa-accumulo-dist_2.11-1.3.2-bin.tar.gz /usr/local/geomesa
```

Copy the JARs to accumulo
```
$ cd /usr/local/geomesa/bin/dist/accumulo
$ sudo cp geomesa-accumulo-distributed-runtime_2.11-1.3.2.jar /usr/local/accumulo/lib/ext/
$ sudo cp geomesa-accumulo-raster-distributed-runtime_2.11-1.3.2.jar /usr/local/accumulo/lib/ext/
```

Update your .bashrc
```
$ vim ~/.bashrc
```
Put these lines into your .bashrc file:
export GEOMESA_ACCUMULO_HOME=/usr/local/geomesa
export PATH=$PATH:/usr/local/geomesa/bin/

Source .bashrc
```
$ . ~/.bashrc
```
Configure namespace:
```
$ $GEOMESA_ACCUMULO_HOME/bin/setup-namespace.sh -u root -n myNamespace
```

```
$ bin/install-jai.sh
$ bin/install-jline.sh
```

Test the command to see if GeoMesa works:
```
$ geomesa version
```

Congratulations! You are done! Now you have GeoMesa running on OpenStack Ubuntu Server. You could also try this GeoMesa tutorial after above steps:
http://www.geomesa.org/documentation/current/tutorials/geomesa-quickstart-accumulo.html