package com.log.parser

import org.apache.spark.sql.SparkSession
import org.scalatest.funsuite.AnyFunSuite
import org.apache.spark.sql.Dataset

class LogParserTest extends AnyFunSuite {
  test("parseLogs should correctly parse valid log lines") {
    val spark = SparkSession.builder
      .appName("LogParserTest")
      .master("local[1]")
      .config("spark.sql.session.timeZone", "UTC")  // Set the timezone to UTC
      .getOrCreate

    import spark.implicits._

    // Test data
    val testLogs: Dataset[String] = spark.createDataset(Seq(
      "184.87.250.135 - - [06/Nov/2024:23:20:37 +0000] \"GET /Integrated/challenge.gif HTTP/1.1\" 200 2344 \"-\" \"Mozilla/5.0(Macintosh; PPC Mac OS X 10_7_2) AppleWebKit/5310 (KHTML, like Gecko)Chrome/39.0.897.0 Mobile Safari/5310\"",
      "192.168.1.1 - - [28/Nov/2024:12:34:56 +0000] \"GET / HTTP/1.1\" 200 1024 \"-\" \"Mozilla/5.0 (Linux; Android 10; Mobile)\"",
      "203.0.113.0 - - [27/Nov/2024:08:12:34 +0000] \"GET /index.html HTTP/1.1\" 404 512 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; Desktop)\"",
      "198.51.100.2 - - [26/Nov/2024:18:45:12 +0000] \"POST /api/login HTTP/1.1\" 401 256 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; Desktop)\"",
      "198.51.100.2 - - [26/Nov/2024:18:47:12 +0000] \"POST /api/login HTTP/1.1\" 401 256 \"-\" \"Mozilla/5.0 (Windows NT 10.0; Win64; Desktop)\""
    ))

    // Expected output
    val expectedData = Seq(
      ("184.87.250.135", "2024-11-06", "Phone", 1),
      ("192.168.1.1", "2024-11-28", "Phone", 1),
      ("203.0.113.0", "2024-11-27", "Desktop", 1),
      ("198.51.100.2", "2024-11-26", "Desktop", 2),
    ).toDF("ip", "date", "device_type", "request_count")

    // Actual output
    val actualData = LogParser.parseLogs(testLogs)(spark)

    // Assert equality
    assert(actualData.collect().toSet == expectedData.collect().toSet)

    spark.stop()
  }
}
