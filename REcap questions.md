# Databricks Interview Questions (Full Set)

## 1. Clusters
### Basic
- What is a cluster in Databricks?
- Difference between All-Purpose Cluster vs Job Cluster.
- What is a driver node and worker node?
- What is auto-scaling?
- What is the difference between high-concurrency cluster and standard cluster?

### Intermediate
- What happens when a cluster is terminated?
- How cluster policies help in enterprise environments?
- Explain cluster modes: Single User, Shared, No Isolation Shared.
- What is the role of Spark executors inside a Databricks cluster?
- Why is DBR (Databricks Runtime) important?

### Advanced
- Your cluster keeps failing while loading large data. What steps will you take?
- If a cluster is slow, how do you diagnose the issue?
- How to choose the correct number of workers for ETL pipelines?
- What is Photon? When to use it?
- How to enforce cost control on clusters?

## 2. Databricks FileStore
- What is FileStore in Databricks?
- FileStore vs DBFS – what is the difference?
- How to upload files manually using the Databricks UI?
- Path difference: `/FileStore`, `/dbfs/FileStore`, `dbfs:/FileStore`.
- How to serve images or HTML files from FileStore?
- Can FileStore be used for production? Why or why not?
- How to access FileStore from Python or Spark code?
- Can you mount external storage to FileStore?
- Why is FileStore preferred for teaching/demo environments?
- What is the size limitation of FileStore in Community Edition?

## 3. Hive Metastore
### Basic
- What is Hive Metastore?
- Role of Metastore in Spark & Databricks.
- Where metadata is stored in Databricks CE vs Premium.
- Difference between managed and external tables.
- What happens when you drop a managed table?

### Intermediate
- How to create a database in Hive Metastore?
- Difference between Hive Metastore vs Unity Catalog.
- How schema and partition info is stored?
- How to repair table metadata?
- How Databricks stores table metadata internally?

### Advanced
- You moved Parquet files manually; how do you refresh metadata?
- Why does a query sometimes show stale metadata?
- How to migrate Hive Metastore tables to Unity Catalog?
- Why Metastore is the brain of the Lakehouse architecture?
- How to create a table using location clause & what happens internally?

## 4. File Types
- Common file formats used in Databricks.
- Difference between Delta, Parquet, ORC.
- Which file format is best for large-scale analytics?
- Why CSV is not recommended for production?
- What is columnar storage?
- How Parquet compresses data?
- Why Delta format is best for ACID?
- Differences between JSON vs XML vs CSV.
- How to read semi-structured data in Databricks?
- Why Delta outperforms Parquet?

## 5. Databricks Security Fundamentals
### Basic
- What is workspace-level security?
- How to create users and groups?
- Cluster permissions types.
- What is token-based authentication?
- What is SCIM?

### Intermediate
- What is Credential Passthrough?
- What is Data Access Control (DAC)?
- Mount vs direct S3 access – which is secure?
- What is Table ACL?
- How to rotate access tokens?

### Advanced
- What is Unity Catalog? Why is it important for governance?
- Explain secure cluster connectivity.
- How Databricks implements zero-trust architecture?
- How to secure ETL pipelines?
- Principle of least privilege in Databricks – how to implement?

## 6. Delta Lake & Data Management
- What is Delta Lake?
- How is Delta different from Parquet?
- What is Delta Log?
- Role of `_delta_log` folder.
- What is schema enforcement?
- What is ACID in Delta?
- How does Delta manage snapshot isolation?
- What is OPTIMIZE and ZORDER?
- How Delta removes small files?
- What is vacuum and retention period?

## 7. Delta Lake Overview
- What is Delta Transaction Log?
- What is batch and streaming unification?
- Explain Delta architecture.
- How Delta maintains versions?
- How MERGE works internally?

## 8. ACID Transactions
### Basic
- What is ACID?
- Why ACID is important in data lakes?
- Example of atomicity.
- Difference between atomicity and consistency.

### Intermediate
- How UPDATE, DELETE, MERGE maintain ACID?
- What is optimistic concurrency control?
- What if two updates happen simultaneously?
- What is isolation level in Delta?

### Advanced
- Explain commit files in `_delta_log`.
- What is idempotent write?
- Why Delta ensures no partial update takes place?

## 9. Schema Evolution
- What is schema enforcement?
- Difference between schema evolution vs schema merging.
- How to enable schema evolution?
- How Delta detects column conflict?
- Why "write incompatible schema" error occurs?
- Real-world example of schema evolution in retail or banking.

## 10. Time Travel
- What is Time Travel?
- How to query older versions?
- Query using version vs timestamp.
- What is a snapshot?
- How long Delta stores history?
- How to restore a table to older version?
- How time travel helps in auditing?

## 11. Optimization
### Basic
- What is OPTIMIZE command?
- What is ZORDER BY?
- What is data skipping?

### Intermediate
- What are small files?
- How does OPTIMIZE solve small files problem?
- What is delta caching?

### Advanced
- When NOT to use ZORDER?
- You have slow queries – how to troubleshoot?
- How to optimize large streaming workloads?
- Why repartitioning helps performance?