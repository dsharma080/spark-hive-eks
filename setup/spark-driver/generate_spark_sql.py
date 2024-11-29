import os
import boto3
import sys

# Fetch the SPARK_MASTER_ENDPOINT environment variable
spark_master_endpoint = os.getenv('SPARK_MASTER_ENDPOINT')

if not spark_master_endpoint:
    print("Error: SPARK_MASTER_ENDPOINT environment variable is not set.")
    exit(1)

# Fetch the SPARK_MASTER_ENDPOINT environment variable
hive_endpoint = os.getenv('HIVE_ENDPOINT')

if not hive_endpoint:
    print("Error: HIVE_ENDPOINT environment variable is not set.")
    exit(1)

# Fetch AWS credentials using boto3
# Create a session to access credentials
session = boto3.Session()
aws_access_key_id = session.get_credentials().access_key
aws_secret_access_key = session.get_credentials().secret_key

if not aws_access_key_id or not aws_secret_access_key:
    raise ValueError("AWS credentials are not available.")

# Define the bash script content
bash_script_content = f"""#!/bin/bash

# Spark SQL command with dynamic master URL from SPARK_MASTER_ENDPOINT
spark-sql \
    --master spark://{spark_master_endpoint}:7077 \
    --packages org.apache.hadoop:hadoop-aws:3.3.2,io.delta:delta-spark_2.12:3.2.0,org.apache.spark:spark-hive_2.12:3.5.1 \
    --conf spark.hadoop.fs.s3a.access.key={aws_access_key_id} \
    --conf spark.hadoop.fs.s3a.secret.key={aws_secret_access_key} \
    --conf spark.hadoop.fs.s3a.endpoint=s3.amazonaws.com \
    --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
    --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
    --conf spark.sql.catalogImplementation=hive \
    --conf spark.hadoop.hive.metastore.uris=thrift://{hive_endpoint}:9083 \
"""

# Write the bash script content to a .sh file
bash_script_filename = "spark_sql_script.sh"
with open(bash_script_filename, 'w') as bash_file:
    bash_file.write(bash_script_content)

# Make the script executable (if running on a Unix-like system)
os.chmod(bash_script_filename, 0o755)

print(f"Bash script '{bash_script_filename}' has been generated successfully.")
