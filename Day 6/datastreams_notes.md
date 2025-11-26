# Data Streams Explained for Data Engineering with Databricks (AWS)

## 1. What Are Data Streams?
Data Streams are continuous, real-time flows of data generated from applications, sensors, devices, logs, transactions, and events. Streams never stop and must be processed continuously.

## 2. Importance in Data Engineering
- Real-time dashboards  
- Fraud detection  
- Alerts and anomaly detection  
- Recommendation systems  
- Continuous ETL  
- IoT telemetry  

Streaming = low-latency, continuous, event-driven pipelines.

---

## 3. Streaming in Databricks (AWS)
Databricks provides enterprise-grade streaming tools:
- Structured Streaming  
- Auto Loader  
- Delta Lake Streaming  
- Delta Live Tables  
- Checkpointing  
- Watermarking  

---

## 4. Core Concepts Students Must Learn

### 4.1 Batch vs Streaming  
Batch → Scheduled, static datasets  
Streaming → Continuous, incremental data

### 4.2 Typical Real-Time Architecture
```
Source → Ingestion → Processing → Storage → Serving → BI/ML
```

AWS Example:
```
Kinesis / Kafka → Databricks Structured Streaming → Delta Lake → Athena/QuickSight
```

---

## 5. AWS Streaming Services
### Amazon Kinesis Data Streams  
High-throughput ingestion (Kafka alternative)

### Amazon Kinesis Firehose  
Near real-time delivery to S3, Redshift, Splunk

### Amazon MSK (Managed Kafka)  
Kafka cluster managed by AWS

---

## 6. Databricks Structured Streaming
Treats streaming data as **unbounded tables**.

Supports:
- Kafka
- Kinesis
- Auto Loader (S3 incremental)
- Directory monitoring

Outputs:
- Delta Lake  
- Kafka  
- File formats  

---

## 7. Auto Loader (CloudFiles)
Simplest way to process continuously arriving files in S3.

Example:
```python
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .load("s3://ittechgenie-raw/events/"))

df.writeStream.format("delta")   .option("checkpointLocation", "/mnt/checkpoints/events")   .outputMode("append")   .start("s3://ittechgenie-bronze/events_delta")
```

---

## 8. Delta Lake for Streaming
Benefits:
- ACID transactions  
- Exactly-once processing  
- Schema inference  
- Schema evolution  
- Time Travel  
- Performance optimizations (ZORDER)  

---

## 9. Checkpoints & State Management
Checkpoints ensure:
- No duplicate processing  
- State recovery  
- Streaming progress tracking  

Stored in:
```
/mnt/checkpoints/streaming_pipeline/
```

---

## 10. Streaming Medallion Architecture
### Bronze  
Raw stream  
### Silver  
Cleaned, validated  
### Gold  
Business aggregates (KPIs)

Streaming → Continuous Medallion ETL

---

## 11. Delta Live Tables (DLT)
DLT automates:
- Pipeline dependency management  
- Quality checks  
- Incremental updates  
- Operational logs  
- Streaming ingestion

---

## 12. Streaming + Machine Learning
Use cases:
- Fraud detection  
- Real-time scoring  
- IoT anomaly detection  
- Recommendation engines  

Databricks + MLFlow allow model scoring in streaming jobs.

---

## 13. Handling Bad Data
- DLQ (dead-letter queue)
- _rescued data_ column  
- Retry logic  
- Auto Loader error handling  

---

## 14. Real-Time Project Example
**Pipeline:**
```
Kinesis → Databricks Structured Streaming → Bronze Delta  
Bronze → Silver (clean)  
Silver → Gold (aggregated)  
Gold → Athena/QuickSight Dashboard
```

---

## Summary
Streaming is essential for real-time analytics. Databricks provides a full ecosystem for streaming ingestion, processing, storage, and pipeline orchestration using Kinesis, Auto Loader, Structured Streaming, and Delta Lake.
