# Mounting with AWS (Databricks) — Markdown Version

## 1. What is Mounting in Databricks?

Mounting = Creating **a permanent folder inside DBFS** that points to an S3 bucket.

**Before Mounting:**
```
spark.read.csv("s3://mybucket/raw/data.csv")
```

**After Mounting:**
```
spark.read.csv("/mnt/mybucket/raw/data.csv")
```

DBFS treats `/mnt/...` like local storage.

---

## 2. Why Mounting is Important

### ✔ Simplified Paths  
Use short paths instead of long S3 URLs.

### ✔ Store Credentials Once  
Use Databricks Secrets to store AWS keys securely.

### ✔ Team Collaboration  
Everyone uses the same folder structure:
```
/mnt/project/raw
/mnt/project/bronze
/mnt/project/silver
/mnt/project/gold
```

### ✔ DBFS Optimization  
DBFS handles retries, throttling, and connection management.

---

## 3. Can You Work Without Mounting?

Yes!

```
spark.read.csv("s3://mybucket/raw/data.csv")
df.write.parquet("s3://mybucket/silver/orders")
```

### But limitations:
- Must provide credentials each time  
- Hard for large teams  
- Hard to maintain many S3 paths  
- No DBFS optimization  

---

## 4. Step-by-Step Mounting Guide

### ✔ Step 1 — Create AWS IAM User/Role

IAM Policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::your-bucket"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": ["arn:aws:s3:::your-bucket/*"]
    }
  ]
}
```

Store:
- AWS_ACCESS_KEY  
- AWS_SECRET_KEY  

---

### ✔ Step 2 — Create Databricks Secret Scope

```
dbutils.secrets.createScope("awscreds")
```

Add:
- Key: access-key  
- Key: secret-key  

---

### ✔ Step 3 — Prepare Variables

```python
access_key = dbutils.secrets.get("awscreds", "access-key")
secret_key = dbutils.secrets.get("awscreds", "secret-key")
encoded_secret = secret_key.replace("/", "%2F")
aws_bucket = "your-bucket-name"
mount_name = "mybucket"
```

---

### ✔ Step 4 — Mount S3 Bucket

```python
dbutils.fs.mount(
    source = f"s3a://{access_key}:{encoded_secret}@{aws_bucket}",
    mount_point = f"/mnt/{mount_name}",
    extra_configs = {
        "fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider"
    }
)
```

---

### ✔ Step 5 — Validate

```
dbutils.fs.ls("/mnt/mybucket")
```

---

### ✔ Step 6 — Read Data

```python
df = spark.read.csv("/mnt/mybucket/raw/orders.csv", header=True)
display(df)
```

---

### ✔ Step 7 — Write Data

```python
df.write.mode("overwrite").parquet("/mnt/mybucket/silver/orders")
```

---

### ✔ Step 8 — Unmount

```
dbutils.fs.unmount("/mnt/mybucket")
```

---

## 5. Real ETL Pipeline (Bronze → Silver → Gold)

### Bronze

```python
raw_df = spark.read.json("/mnt/myproject/raw")
raw_df.write.mode("overwrite").format("delta").save("/mnt/myproject/bronze/orders")
```

### Silver

```python
bronze_df = spark.read.format("delta").load("/mnt/myproject/bronze/orders")
silver_df = bronze_df.filter("status = 'complete'")
silver_df.write.mode("overwrite").format("delta").save("/mnt/myproject/silver/orders")
```

### Gold

```python
silver_df = spark.read.format("delta").load("/mnt/myproject/silver/orders")
gold_df = silver_df.groupBy("customer_id").sum("amount")
gold_df.write.mode("overwrite").format("parquet").save("/mnt/myproject/gold/customer_sales")
```

---

## 6. Should You Mount?

| Feature | With Mount | Without Mount |
|--------|----------|----------|
| Simple paths | ✔ | ❌ |
| One-time credential setup | ✔ | ❌ |
| Best for ETL | ✔ | ❌ |
| Direct S3 read/write | ✔ | ✔ |

---

## ✔ Final Conclusion
Mounting is highly recommended for collaborative ETL projects.  
Direct S3 access is fine for temporary workloads or CE.

