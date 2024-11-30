### Overview 
This project intends to achieve following -
- Set up Spark and Hive on Amazon EKS using Terraform 
- Use an ec2 instance as spark driver and run following - 
   + Spark job to read s3 Nginx logs and store the processed version in delta format in s3 itself. 
   + Run Spark SQL queries on Hive on the processed data 

![Architecture diagram](./docs/aws-eks.jpg?raw=true)

### Pre requisites
* aws-cli 
* kubectl
* terraform 
* spark 3.5.1 
* Putty

### Setup 

Note the setup is done for Windows powershell. Please make changes accordingly for your OS environment. 

#### Setup EKS 
```
cd setup/terraform
terraform init 
terraform apply 
python update_perms.py
```
Export the variables 
```
$env:RDS_ENDPOINT = <rds_endpoint_output>
$env:SPARKDRIVER_IP = <sparkdriver_ip_output>
```
#### Setup Spark 
```
cd setup/spark
aws eks --region ap-south-1 update-kubeconfig --name spark-eks-granica
kubectl apply -f spark.yaml
kubectl apply -f spark-master-service.yaml
```
Export the spark driver service endpoint (extract using `kubectl get services`)
```
$env:SPARK_MASTER_ENDPOINT=<master_endpoint>
```
#### Setup Hive Meta Store 
We need to first setup the Hive database on the RDS endpoint - 
```
cd setup/hive
./rds_schema.bat
```
Now generate the hive-site.xml file and build the docker image (make sure docker engine is started)
```
cd setup/hive
./hive_setup.bat
```
Export the hive service endpoint (extract using `kubectl get services`)
```
$env:HIVE_ENDPOINT=<hive_endpoint>
```

#### Spark driver setup
Create the jar file 
```
cd data-pipeline/log-parser
sbt assembly // or do via Intellij
```

Set .ppk file path which is used by pscp
```
$env:PPK_FILE=<path_to_ppk_file>
```

Transfer the files to the spark driver machine
```
cd setup/spark-driver
./generate_bash_script.bat
./copy-files.bat
```

### Data processing 
Once spark driver machine is set up, you can run following to process the input log files 
```
./spark_submit_script.sh s3a://granica-assignment/input-files/input1.txt s3a://granica-assignment/delta-output
```

### Hive queries 
You can run hive queries in `spark-sql`. To start the shell - 
```
./spark_sql_script.sh
```

First time we will have to create the table as below 
```
CREATE TABLE delta_table USING delta LOCATION 's3a://granica-assignment/delta-output/';
```

Queries 
1. Top 5 IPs daily 
```
SELECT ip, date, total_request_count
FROM (
  SELECT 
    ip, 
    date, 
    SUM(request_count) AS total_request_count,
    ROW_NUMBER() OVER (PARTITION BY date ORDER BY SUM(request_count) DESC) AS rank
  FROM delta_table
  GROUP BY ip, date
) ranked_data
WHERE rank <= 5
ORDER BY date, rank;

```

2. Top 5 device_type daily
```
SELECT device_type, date, total_request_count
FROM (
  SELECT 
    device_type, 
    date, 
    SUM(request_count) AS total_request_count,
    ROW_NUMBER() OVER (PARTITION BY date ORDER BY SUM(request_count) DESC) AS rank
  FROM requests
  GROUP BY device_type, date
) ranked_data
WHERE rank <= 5
ORDER BY date, rank;

```

3. Top 5 IPs weekly 
```
SELECT ip, week, total_request_count
FROM (
  SELECT 
    ip, 
    WEEKOFYEAR(date) AS week, 
    SUM(request_count) AS total_request_count,
    ROW_NUMBER() OVER (PARTITION BY WEEKOFYEAR(date) ORDER BY SUM(request_count) DESC) AS rank
  FROM requests
  GROUP BY ip, WEEKOFYEAR(date)
) ranked_data
WHERE rank <= 5
ORDER BY week, rank;

```

4. Top 5 device_type weekly 
```
SELECT device_type, week, total_request_count
FROM (
  SELECT 
    device_type, 
    WEEKOFYEAR(date) AS week, 
    SUM(request_count) AS total_request_count,
    ROW_NUMBER() OVER (PARTITION BY WEEKOFYEAR(date) ORDER BY SUM(request_count) DESC) AS rank
  FROM requests
  GROUP BY device_type, WEEKOFYEAR(date)
) ranked_data
WHERE rank <= 5
ORDER BY week, rank;
```
