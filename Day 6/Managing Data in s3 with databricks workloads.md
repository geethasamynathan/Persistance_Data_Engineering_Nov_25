# Managing Data in Amazon S3 with Databricks Workloads

## 1. Introduction
Amazon S3 is the central data lake for AWS. Databricks reads and writes data directly to S3 for ETL workloads.

## 2. What is “Managing Data in S3 with Databricks Workloads”?
- Reading data from S3
- Writing data to S3
- Managing permissions via IAM roles
- Delta Lake ACID operations
- Medallion architecture
- Workflows and automation

## 3. Why Use S3 with Databricks?
- Scalable, low-cost storage
- High durability
- Compute–storage separation
- Delta Lake support
- Ideal for lakehouse architecture

## 4. Alternatives
- Databricks Filestore
- Unity Catalog Volumes
- DBFS Root
- Azure ADLS
- Google Cloud Storage

## 5. How Databricks Connects to S3
Using IAM Instance Profiles:
Databricks → IAM Role → S3 bucket permissions.

## 6. Step-by-Step Setup
### Step 1 — Create S3 Bucket
### Step 2 — Create IAM Role
### Step 3 — Add Role to Databricks
### Step 4 — Attach Role to Cluster
### Step 5 — Verify in Notebook

## 7. Reading and Writing Data
### Read:
```python
df = spark.read.csv("s3://mycompany-datalake/raw/sales.csv", header=True, inferSchema=True)
```

### Write Delta:
```python
df.write.format("delta").mode("overwrite").save("s3://mycompany-datalake/bronze/sales_delta")
```

## 8. Real-World Pipeline Example
Bronze → Silver → Gold ETL for Sales Analytics.

## 9. Advanced Operations
- OPTIMIZE
- ZORDER
- Time travel
- Schema evolution

## 10. Databricks Community Edition Notes
CE cannot mount S3. Use public URLs or presigned URLs.

## 11. Best Practices
- Use Instance Profiles
- Organize bucket with Bronze/Silver/Gold
- Avoid small files
- Use Auto Loader

## 12. Summary
A full workflow for managing S3 data with Databricks.

