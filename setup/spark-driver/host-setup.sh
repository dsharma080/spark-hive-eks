#!/bin/bash
sudo apt update
sudo apt install -y openjdk-11-jdk wget scala
wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar -xzf spark-3.5.1-bin-hadoop3.tgz
sudo mv spark-3.5.1-bin-hadoop3 /opt/spark
echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo "export PATH=/opt/spark/bin:$PATH" >> ~/.bashrc
source ~/.bashrc