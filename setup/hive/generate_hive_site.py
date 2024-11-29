import os
import xml.etree.ElementTree as ET
import boto3

# Create a session using the default profile
session = boto3.Session()

# Get AWS credentials
aws_access_key = session.get_credentials().access_key
aws_secret_key = session.get_credentials().secret_key

# Fetching environment variables
rds_endpoint = os.getenv('RDS_ENDPOINT')

print(rds_endpoint, aws_access_key, aws_secret_key)
# Check if required environment variables are set
if not rds_endpoint or not aws_access_key or not aws_secret_key:
    print("Error: Required variables (RDS_ENDPOINT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are not set.")
    exit(1)

# Split RDS_ENDPOINT into host and port
host = rds_endpoint
port = 3306

# Create XML structure
configuration = ET.Element('configuration')

# JDBC Connection Configuration
jdbc_connection_url = ET.SubElement(configuration, 'property')
ET.SubElement(jdbc_connection_url, 'name').text = 'javax.jdo.option.ConnectionURL'
ET.SubElement(jdbc_connection_url, 'value').text = f'jdbc:mysql://{host}:{port}/hivemetastore'

jdbc_driver_name = ET.SubElement(configuration, 'property')
ET.SubElement(jdbc_driver_name, 'name').text = 'javax.jdo.option.ConnectionDriverName'
ET.SubElement(jdbc_driver_name, 'value').text = 'com.mysql.cj.jdbc.Driver'

jdbc_user_name = ET.SubElement(configuration, 'property')
ET.SubElement(jdbc_user_name, 'name').text = 'javax.jdo.option.ConnectionUserName'
ET.SubElement(jdbc_user_name, 'value').text = 'hive_test'

jdbc_password = ET.SubElement(configuration, 'property')
ET.SubElement(jdbc_password, 'name').text = 'javax.jdo.option.ConnectionPassword'
ET.SubElement(jdbc_password, 'value').text = 'hive_password'

# Hive Warehouse Configuration
warehouse_dir = ET.SubElement(configuration, 'property')
ET.SubElement(warehouse_dir, 'name').text = 'hive.metastore.warehouse.dir'
ET.SubElement(warehouse_dir, 'value').text = 's3a://granica-assignment/hive/warehouse'

# S3 Configuration
s3_access_key = ET.SubElement(configuration, 'property')
ET.SubElement(s3_access_key, 'name').text = 'fs.s3a.access.key'
ET.SubElement(s3_access_key, 'value').text = aws_access_key

s3_secret_key = ET.SubElement(configuration, 'property')
ET.SubElement(s3_secret_key, 'name').text = 'fs.s3a.secret.key'
ET.SubElement(s3_secret_key, 'value').text = aws_secret_key

s3_endpoint = ET.SubElement(configuration, 'property')
ET.SubElement(s3_endpoint, 'name').text = 'fs.s3a.endpoint'
ET.SubElement(s3_endpoint, 'value').text = 's3.amazonaws.com'

s3_impl = ET.SubElement(configuration, 'property')
ET.SubElement(s3_impl, 'name').text = 'fs.s3a.impl'
ET.SubElement(s3_impl, 'value').text = 'org.apache.hadoop.fs.s3a.S3AFileSystem'

s3_multipart = ET.SubElement(configuration, 'property')
ET.SubElement(s3_multipart, 'name').text = 'fs.s3a.multipart.uploads.enabled'
ET.SubElement(s3_multipart, 'value').text = 'true'

s3_path_style = ET.SubElement(configuration, 'property')
ET.SubElement(s3_path_style, 'name').text = 'fs.s3a.path.style.access'
ET.SubElement(s3_path_style, 'value').text = 'false'

# Generate XML string
tree = ET.ElementTree(configuration)

# Write to file
with open('hive-site.xml', 'wb') as f:
    tree.write(f)

print("XML configuration file 'hive-site.xml' generated successfully.")
