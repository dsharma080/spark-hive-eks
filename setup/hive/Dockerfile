FROM apache/hive:3.1.3

# Download the MySQL Connector JAR
COPY ./jars/mysql-connector-java-8.0.15.jar /opt/hive/lib/
COPY ./jars/hadoop-aws-3.2.0.jar /opt/hive/lib/
COPY ./jars/aws-java-sdk-bundle-1.11.375.jar /opt/hive/lib/

# Set the CLASSPATH environment variable to include necessary JARs
ENV HIVE_CLASSPATH=/opt/hive/lib/mysql-connector-java-8.0.15.jar:/opt/hive/lib/hadoop-aws-3.2.0.jar:/opt/hive/lib/aws-java-sdk-bundle-1.11.375.jar

# Copy the updated hive-site.xml
COPY hive-site.xml /opt/hive/conf/

# Start the Hive Metastore service
ENTRYPOINT ["hive", "--service", "metastore"]
