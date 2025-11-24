# Topic 3 — Hive Metastore (Detailed Q&A + Practical Real-World Scenarios)

## 1. What is Hive Metastore in Databricks?
Hive Metastore is a central metadata repository that stores table definitions, schemas, locations, partition info, and statistics.  
It stores metadata, not data, and Spark/Databricks depends on it for SQL operations.

### Practical Behavior
Running:
```sql
SHOW TABLES IN default;
```
Fetches table metadata from the Hive Metastore, not storage files.

---

## 2. What is stored inside Hive Metastore?
Hive Metastore contains metadata like:
- Database names  
- Table names  
- Column names & data types  
- Partition definitions  
- Table file locations  
- Views and table properties  

### Behavior Example
Renaming a column:
```sql
ALTER TABLE sales RENAME COLUMN amount TO revenue;
```
Updates *only* metadata.

---

## 3. Where is Hive Metastore stored in Databricks?

### Community Edition
Stored in **local DBFS** (reset if workspace resets).

### Premium/Enterprise
Can be:
- Workspace-local  
- External database (RDS/Azure SQL)  
- Unity Catalog Metastore  

### Practical Behavior
Workspace reset → metadata lost (CE only).

---

## 4. Managed Tables vs External Tables

| Feature | Managed Table | External Table |
|--------|---------------|----------------|
| Storage | Warehouse folder | External location (S3/ADLS/FileStore) |
| DROP TABLE | Deletes data + metadata | Deletes metadata only |
| Use Case | Temporary/POC | Production-grade |

### Example
Managed:
```sql
CREATE TABLE sales_managed AS SELECT * FROM df;
```
External:
```sql
CREATE TABLE sales_ext LOCATION 'dbfs:/mnt/sales/' AS SELECT * FROM df;
```

---

## 5. What happens when you DROP a managed table?
- Metadata removed  
- Data files deleted  
- Warehouse directory removed  

External table → **files remain**.

---

## 6. How to create a database in Hive Metastore?

```sql
CREATE DATABASE sales_db;
```

Custom location:
```sql
CREATE DATABASE sales_db LOCATION 'dbfs:/mnt/enterprise/sales_db/';
```

### Behavior
Creates folder + metadata entry.

---

## 7. How to check metadata for a table?
```sql
DESCRIBE DETAIL sales.orders;
```
Shows:
- Table location  
- Format  
- Schema  
- File count  
- Statistics  

---

## 8. Hive Metastore vs Unity Catalog

| Feature | Hive Metastore | Unity Catalog |
|---------|----------------|----------------|
| Governance | Basic | Enterprise |
| Security | Table-level | Column & Row-level |
| Lineage | No | Yes |
| Sharing | Limited | Delta Sharing |
| Structure | DB → Table | Catalog → Schema → Table |

Unity Catalog is the enterprise standard.

---

## 9. Repairing Hive Metastore when partitions are missing
Use:
```sql
MSCK REPAIR TABLE sales_partitioned;
```

### Behavior
Scans directories → identifies partitions → updates metadata.

---

## 10. Why does a query show stale metadata?

### Causes
- Manual file operations  
- Parquet schema change  
- Missing refresh  
- Cache issues  

### Fix
```sql
REFRESH TABLE sales;
```

---

## 11. How Spark reads a table using Hive Metastore
Execution steps:
1. Fetch schema  
2. Fetch location  
3. Read files  
4. Apply filters  
5. Return result  

Missing metadata → error:
```
TABLE_OR_VIEW_NOT_FOUND
```

---

## 12. Real-World Scenario: Files Added but Not Showing
You add files manually into:
```
/mnt/data/sales/date=2024-11-01/
```
But queries show no new rows.

### Fix
```sql
MSCK REPAIR TABLE sales;
```

---

## 13. Scenario: Metastore deleted – Is data lost?
No.

Re-register table:
```sql
CREATE TABLE sales USING delta LOCATION 'dbfs:/mnt/sales/';
```
Metadata restored.

---

## 14. Migrating Hive Metastore tables to Unity Catalog

### Step 1 – Create Schema
```sql
CREATE CATALOG main;
CREATE SCHEMA main.sales;
```

### Step 2 – Register external data
```sql
CREATE TABLE main.sales.orders USING delta LOCATION 'dbfs:/mnt/sales/orders';
```

### Step 3 – Assign permissions
```sql
GRANT SELECT ON TABLE main.sales.orders TO `users`;
```

---

## 15. Practical Exercise: Find Table Storage Location
```sql
DESCRIBE DETAIL sales;
```

### Behavior
Shows:
```
"location": "dbfs:/user/hive/warehouse/sales"
```

---

## End of Topic 3 – Hive Metastore
This topic includes:
- Detailed explanations  
- Practical scenarios  
- Troubleshooting patterns  
- SQL & PySpark examples  
