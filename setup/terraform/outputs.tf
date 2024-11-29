output "RDS_ENDPOINT" {
  value = regex("^([^:]+)", aws_db_instance.hive_metastore_db.endpoint)
}

output "SPARKDRIVER_IP" {
  value = aws_instance.spark_driver.public_ip
}
