# Topic 4 — File Types (Delta vs Parquet vs CSV vs JSON)

## 1. Common File Types in Databricks
Databricks most commonly uses:
- **Delta** – Transactional, ACID-compliant, versioned
- **Parquet** – Columnar, compressed, analytical
- **CSV** – Row-based, plain text
- **JSON** – Semi-structured, nested data
- **ORC** – Columnar format used in Hadoop environments

Databricks automatically recognizes file type based on extension.

---

## 2. What is Parquet and Why is it Used?
Parquet is a **columnar storage format** optimized for:
- Efficient compression  
- Fast reads  
- Predicate pushdown  
- Analytics workloads  

### Practical Behavior
A query like:
```python
df.select("customer_id").show()
```
Reads only **customer_id** column, not entire row.

---

## 3. What is Delta Lake? How is it Different from Parquet?
Delta Lake = Parquet + Transaction Log (`_delta_log`)

### Delta Features
- ACID transactions  
- Time Travel  
- Schema Enforcement  
- Schema Evolution  
- Data versioning  
- MERGE, UPDATE, DELETE  

### Comparison

| Feature | Parquet | Delta |
|--------|---------|--------|
| ACID | ❌ | ✔ |
| MERGE | ❌ | ✔ |
| Time Travel | ❌ | ✔ |
| Schema Evolution | Partial | Full |
| Data Lineage | ❌ | ✔ |

---

## 4. What Happens Internally When Writing a Delta Table?

```python
df.write.format("delta").save("/mnt/delta/sales")
```

Delta:
1. Writes Parquet files  
2. Creates metadata JSON in `_delta_log`  
3. Generates versioned commit files  
4. Manages concurrency using OCC (Optimistic Concurrency Control)

### Behavior
If two users write simultaneously → one gets:
```
ConcurrentModificationException
```

---

## 5. Why CSV is Not Recommended for Production?
CSV:
- Has no schema  
- No compression  
- Error-prone  
- Slow reads  
- No ACID  
- Larger file size  
- Does not support nested data  

### Practical Behavior
Inferring schema:
```python
spark.read.csv(path, inferSchema=True)
```
is expensive.

---

## 6. JSON – When to Use?
Ideal for:
- Logs  
- API responses  
- Nested structures  
- Event data  

### Practical Example
```python
df = spark.read.json("/FileStore/json/logs.json")
df.printSchema()
```

---

## 7. Which File Type is Fastest for Analytics?
**Parquet (or Delta)**

Reasons:
- Columnar  
- Compressed  
- Efficient encoding  
- Predicate pushdown  

### Example
```sql
SELECT COUNT(*) FROM sales_parquet WHERE state = 'CA';
```

Spark only reads required columns.

---

## 8. Real Scenario – Why CSV is Slow?
CSV:
- Row-based  
- Must scan entire row  
- No metadata  

Parquet:
- Reads only needed columns  
- Much faster for aggregations  

Performance example (100M rows):
- CSV → 30–60s  
- Parquet → 3–7s  
- Delta → 3–7s with ACID  

---

## 9. How Delta Handles Schema Changes?

Enable schema evolution:
```python
df.write.option("mergeSchema", "true")
  .format("delta")
  .mode("append")
  .save(path)
```

### Behavior
Delta:
- Detects new columns  
- Updates schema  
- Maintains existing Parquet files

---

## 10. What is Time Travel in Delta?
Allows querying older versions of a table.

### Example
```sql
SELECT * FROM sales VERSION AS OF 5;
```
or
```sql
SELECT * FROM sales TIMESTAMP AS OF "2024-11-20";
```

### Use Cases
- Auditing  
- Debugging  
- Data recovery  

---

## 11. Practical Exercise — Convert CSV to Parquet and Delta
### CSV → Parquet
```python
spark.read.csv("dbfs:/FileStore/sales.csv", header=True)     .write.parquet("dbfs:/mnt/sales_parquet")
```

### CSV → Delta
```python
spark.read.csv("dbfs:/FileStore/sales.csv", header=True)     .write.format("delta").save("/mnt/delta/sales")
```

Delta folder contains:
```
/mnt/delta/sales/
  part-00000.parquet
  part-00001.parquet
  _delta_log/
```

---

## 12. What Happens If Folder Contains Mixed File Types?
Example folder:
```
data1.parquet
data2.csv
data3.json
```

### Behavior
Spark either:
- Throws **incompatible file format** error  
or  
- Reads only first valid file extension

---

## 13. Why Delta is Best for Lakehouse?
- ACID  
- Time Travel  
- Schema enforcement  
- Streaming + batch  
- Optimization (ZORDER)  
- Auto-compaction  
- Multi-cloud support  

---

# End of Topic 4 – File Types
