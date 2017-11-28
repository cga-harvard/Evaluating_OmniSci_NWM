###### Author: Charles Thao

This project deploys GeoMesa on OpenStack Cloud

1. SSH to geo_test_2
```
ssh -i ~/.ssh/geo_key.pem ubuntu@128.31.22.28
```

2. What is going on there?

```
On the server, there is an installation of GeoMesa, Spark, Accumulo and Hadoop. Some data is available there, with an inactive instance of GeoServer and .shp files.
```

3. How to use GeoMesa for Tweets Analytics?

GeoMesa has a simple feature to parse tweets in json format, such as the ones in part-00000 output of the Tweet Harvesting Python Spark script

```
geomesa ingest -u USERNAME -c CATALOG -s twitter -C twitter-place-centroid hdfs://namenode:port/path/to/twitter/*
geomesa ingest -u USERNAME -c CATALOG -s twitter -C twitter-place-polygon hdfs://namenode:port/path/to/twitter/*
geomesa ingest -u USERNAME -c CATALOG -s twitter -C twitter hdfs://namenode:port/path/to/twitter/*

```
I have parsed a lot of tweets in the past and was able to map them using GeoServer. Keep in mind that data ingested into GeoMesa will be stored in Accumulo Store, which can be viewed at PUBLICIP:50070.  However, due to a technical difficulty (updating Hadoop without backing up data), all data was lost on Accumulo. It was not a significant amount, and most data can be replicated quickly. 

When there is GeoMesa data in Accumulo, 

4. On geo_test_2, it is also possible to parse tweets directly to OpenStack Swift. Assuming that there is an Accumulo catalog called tweets.
```
geomesa ingest -u USERNAME -c tweets -s twitter -C twitter-place-centroid swift://namenode:port/path/to/twitter/*
```

In order to configure this, the following change must happen to hadoop core site.

Edit /usr/local/hadoop/etc/hadoop/core-site.xml
```
<property>
    <name>fs.swift.impl</name>
    <value>org.apache.hadoop.fs.swift.snative.SwiftNativeFileSystem</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.auth.endpoint.prefix</name>
    <value>/endpoints/AUTH_</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.auth.url</name>
    <value>https://engage1.massopen.cloud:5000/v2.0/tokens/</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.http.port</name>
    <value>8080</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.https.port</name>
    <value>443</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.public</name>
    <value>true</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.tenant</name>
    <value>PROJECT_NAME</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.username</name>
    <value>USERNAME</value>
  </property>
  <property>
    <name>fs.swift.service.sahara.password</name>
    <value>PASSWORD</value>
  </property>

```

5. In order to export files from GeoMesa 
```
geomesa export -u <username> -p <password> \
  -i <instance> -z <zookeepers> \
  -c CATALOG -f csv \
``` 

Interpretation: Export catalog from an Accumulo instance to file with format csv. GeoMesa also allow export to shp, json, and gml file. 
The shp format also requires the -o option to specify the name of an output file. 
