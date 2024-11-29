package com.log.parser

import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.Dataset
import org.apache.spark.sql.functions.{count, date_format, from_utc_timestamp, regexp_extract, to_timestamp, udf}
import nl.basjes.parse.useragent.UserAgentAnalyzer

object LogParser {
  private val uaa = UserAgentAnalyzer.newBuilder().build()

  private val extractDeviceType = udf((userAgent: String) => {
    val agent = uaa.parse(userAgent)
    agent.getValue("DeviceClass") // e.g., Mobile, Tablet, Desktop
  })

  def main(args: Array[String]): Unit = {
    // Validate input arguments
    if (args.length != 2) {
      System.err.println("Usage: Main <input-s3-path> <output-s3-path>")
      System.exit(1)
    }

    val inputPath = args(0)
    val outputPath = args(1)

    // Create a Spark session
    val spark = SparkSession.builder
      .appName("LogParser")
      .config("spark.sql.session.timeZone", "UTC")  // Set the timezone to UTC
      .getOrCreate
    spark.sparkContext.setLogLevel("ERROR")

    import spark.implicits._

    // Read the log file
    val logData = spark.read.text(inputPath).as[String]

    // Parse logs
    val parsedLogs = parseLogs(logData)(spark)

    // Write to Delta table partitioned by date
    parsedLogs.write
      .format("delta")
      .partitionBy("date")
      .mode("append") // assuming called with new log files every time
      .save(outputPath)

    println(s"Data successfully written to Delta table at $outputPath")

    spark.stop()
  }

  /**
   * Parses log data into a DataFrame with columns: date, ip, device_type, request_count
   * @param dataset Input dataset of log lines
   * @return DataFrame with extracted fields
   */
  def parseLogs(dataset: Dataset[String])(implicit spark: SparkSession): DataFrame = {
    import spark.implicits._

    val logPattern =
      """^(\S+) - - \[(.*?)\] ".*?" \d{3} \d+ "-" "(.*?)"$"""
    val timestampFormat = "dd/MMM/yyyy:HH:mm:ss Z"

    dataset
      .select(
        regexp_extract($"value", logPattern, 1).as("ip"),
        regexp_extract($"value", logPattern, 2).as("timestamp"),
        regexp_extract($"value", logPattern, 3).as("user_agent")
      )
      .withColumn("date", date_format(to_timestamp($"timestamp", timestampFormat), "yyyy-MM-dd"))
      .withColumn("device_type", extractDeviceType($"user_agent"))
      .groupBy("ip", "date", "device_type")
      .agg(count("*").as("request_count"))
  }
}
