# MapD_on_MOC

## MapD Database & Visual Analytics Platform (Community Edition) on Amazon

The MapD Core database and Immerse visual analytics platform allows you to query and visualize billions of rows in milliseconds using Amazon's GPU instances, delivering orders-of-magnitude speedups over CPU solutions.

Highlights:

- Millisecond query response times over billions of rows
- Intuitive interaction - standard SQL or MapD's user-friendly dashboards
- Fast, scalable visual analytics

        Operating System: Linux/Unix, CentOS 7.2
        Delivery Method: 64-bit Amazon Machine Image (AMI) 
        AWS Services Required: Amazon EC2, Amazon EBS

## Usage Instruction:

Access the application via a browser at https://<public_dns>:8443. Username is mapd, password will be the same as the instance-id. To connect to the operating system, use SSH and the username centos. The SQL CLI mapdql may be accessed by connecting to the instance via SSH and then running:

/raidStorage/prod/mapd/bin/mapdql -u mapd -p {instance-id}

## EC2 Instance type options:

### p2.xlarge

    Memory: 61GiB
    CPU: 12 EC2 Compute Units (4 virtual cores), plus 1 NVIDIA K80 (GK210) GPU
    Storage: EBS Only
    Platform: 64-bit
    Network Performance: High
    API Name: p2.xlarge
    
### p2.16xlarge

    Memory: 732GiB
    CPU: 188 EC2 Compute Units (64 virtual cores), plus 16 NVIDIA K80 (GK210) GPUs
    Storage: EBS Only
    Platform: 64-bit
    Network Performance: 20 Gigabit Ethernet
    API Name: p2.16xlarge
    
### p2.8xlarge

    Memory: 488GiB
    CPU: 94 EC2 Compute Units (32 virtual cores), plus 8 NVIDIA K80 (GK210) GPUs
    Storage:EBS Only
    Platform: 64-bit
    Network Performance: 10 Gigabit Ethernet
    API Name: p2.8xlarge
    
## Running the ETL scripts:

# Required libraries

The following libraries are required to run the ETL sscripts:
- xarray
- pymapd
- pyarrow==0.7.1
- numpy==1.14.1
- pandas==0.22.0
- pyproj
- mzgeohash

The required libraries could be installed from requirements.txt using:

        pip install -r requirements.txt

