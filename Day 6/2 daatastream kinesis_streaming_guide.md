# Kinesis to S3 Data Streaming — Step-by-Step Guide

## 1. Create an S3 Bucket
Example:
```
ittechgenie-streaming-bucket/kinesis-data/
```

## 2. Create a Kinesis Data Stream
Name:
```
ittechgenie-stream-stream
```
Use **1 shard** or **on-demand** mode.

## 3. Create a Kinesis Firehose Delivery Stream
- Source: **Kinesis Data Stream**
- Destination: **Amazon S3**
- S3 Path:
```
s3://ittechgenie-streaming-bucket/kinesis-data/
```
- Buffer Size: **1 MB**
- Buffer Interval: **60 seconds**
- Format: **JSON**
- IAM Role: Auto-create

## 4. Send Events into Kinesis (Python Producer)

```python
import boto3, json, time, random

kinesis = boto3.client("kinesis", region_name="us-east-1")

while True:
    event = {
        "event_id": random.randint(1000, 9999),
        "customer_id": random.randint(1, 50),
        "amount": round(random.uniform(10, 500), 2),
        "timestamp": int(time.time())
    }
    print("Sending:", event)

    kinesis.put_record(
        StreamName="ittechgenie-stream-stream",
        Data=json.dumps(event),
        PartitionKey="partition-1"
    )

    time.sleep(1)
```

## 5. Verify Delivery
Check:
- Kinesis Stream → Incoming records
- Firehose → Monitoring → Delivery success
- S3 Bucket → New gz/json files every minute

## 6. (Optional) Ingest S3 Streaming Files into Databricks with Auto Loader

```python
df = (spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "json")
      .load("s3://ittechgenie-streaming-bucket/kinesis-data/"))

df.writeStream   .format("delta")   .option("checkpointLocation", "/mnt/checkpoints/kinesis")   .start("/mnt/delta/bronze/kinesis")
```

## Architecture
```
Producer → Kinesis Stream → Firehose → S3 → (Optional) Databricks
```
