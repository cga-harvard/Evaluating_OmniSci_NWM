### Tweet Harvesting on Spark/ Hadoop and OpenStack

### Environment setup
This installation runs on Hadoop 2.7.4 and Spark 2.11.8
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
$ wget http://apache.claz.org/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz
$ tar -xvzf ~/Downloads/hadoop-2.7.4.tar.gz 
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
You should get output similar to below. If Namenode isn't there, then there must be an error when in "hdfs namenode -format":
```
21097 SecondaryNameNode
20772 NameNode
14036 Jps
20917 DataNode
```
In that case, doing the following could help:
```
$ cd $HADOOP_HOME
$ rm -r hdfs_storage/
$ stop-all.sh
$ hadoop namenode -format
$ start-dfs.sh
```

On Horizon, add a rule in your security group that allows access to port 50070(hadoop)
On your browser, go to http://[your-server-IP]:50070 to make sure everything is up and running

###Installing Spark
1. Setup Spark
```
sudo apt-get install scala
wget "http://apache.claz.org/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz"
tar -xvzf spark-2.2.0-bin-hadoop2.7.tgz
sudo mkdir /usr/local/spark
mv ./spark-2.2.0-bin-hadoop2.7/ /usr/local/spark/
```
2. Setup environmental variables
```
export PATH = $PATH:/usr/local/spark/bin
export SPARK_HOME=/usr/local/spark
```
3. Edit /usr/local/spark/conf/spark-env.sh
```
export HADOOP_CONF_DIR=/usr/local/hadoop/conf/
export LD_LIBRARY_PATH=/usr/local/hadoop/lib/native/
export JAVA_LIBRARY_PATH=/usr/local/hadoop/lib/native
export PYSPARK_PYTHON=python3.5
```


###Testing
1. Get the requirements.txt

2. Install the requirements
```
pip3 install -r requirements.txt
```
3. Create a new directory called tweets in the directory where you store TweetsRead and SparkDemo
4. In one terminal, run 
```
spark-submit TweetsRead.py
```
5. Open another terminal, run
```
spark-submit SparkDemo.py
```