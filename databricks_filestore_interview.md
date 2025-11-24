# Databricks FileStore – Interview Questions with Detailed Answers & Practical Scenarios

## 1. What is Databricks FileStore?
FileStore is a special folder inside DBFS (Databricks File System) used to store small user-uploaded files such as CSV, images, HTML files, or documents.  
It is easy to access from both notebooks and browser URLs.

**Paths:**  
- `dbfs:/FileStore/`  
- `/dbfs/FileStore/` (Python file API)  
- `/FileStore/...` (public browser path)

### Practical Behavior
If you upload a file like `sales.csv`, it becomes available at:
```
/FileStore/sales.csv
```
And accessible in browser:
```
https://<workspace>/files/sales.csv
```

---

## 2. FileStore vs DBFS
**DBFS** is the full Databricks storage filesystem.  
**FileStore** is just a user-facing folder for small file uploads.

### Behavior
Running:
```python
dbutils.fs.ls("dbfs:/")
```
Shows:
```
FileStore/
databricks-datasets/
user/
tmp/
```

---

## 3. How to Upload Files to FileStore

### Method 1 — UI Upload
1. Go to **Data** → **Upload File**
2. Select file (CSV, JSON, Excel)
3. It is stored at:
```
/FileStore/tables/<filename>
```

### Method 2 — Programmatically
```python
dbutils.fs.put("/FileStore/mytext.txt", "Hello World", True)
```

---

## 4. File Types Supported in FileStore
You can upload:
- CSV, JSON, TXT
- HTML, JS, CSS
- Images (PNG/JPG)
- Pickle files
- Small ML artifacts

Not suitable for:
- Large datasets
- Production pipelines

---

## 5. Reading FileStore Files in Spark
```python
df = spark.read.csv("dbfs:/FileStore/tables/sales.csv", header=True, inferSchema=True)
display(df)
```

### Behavior
Very fast for small demo datasets but not fault-tolerant.

---

## 6. Serving Files or Images Publicly via FileStore
If stored at:
```
/FileStore/images/demo.png
```
You can view it:
```
https://<workspace>/files/images/demo.png
```

---

## 7. Is FileStore Production Ready?
**No.**

Reasons:
- Small size limit
- No ACID transactions
- No version control
- Not governed by Unity Catalog
- Not distributed or scalable

Best for:
- Training  
- Demos  
- POCs  
- Learning notebooks  

---

## 8. FileStore Size Limit
In Community Edition:
- Total: ~1–2 GB  
- Single file best < 300–500 MB  

Uploading large files results in:
```
java.io.IOException: No space left on device
```

---

## 9. Difference Between dbfs:/, /dbfs/, and /FileStore/

### 1. dbfs:/FileStore/
Used by Spark APIs:
```python
dbutils.fs.ls("dbfs:/FileStore")
```

### 2. /dbfs/FileStore/
Used by Python `open()` APIs:
```python
open("/dbfs/FileStore/file.txt")
```

### 3. /FileStore/
Used for browser access:
```
<img src="/files/example.png">
```

---

## 10. Why You Cannot See an Uploaded File
Possible causes:
- Uploaded to `/FileStore/tables` but looking at `/FileStore`
- Using wrong path prefix
- CE storage may be full

Clear FileStore:
```python
dbutils.fs.rm("dbfs:/FileStore", recurse=True)
```

---

## 11. What Happens If Two Users Write to Same FileStore Path?
FileStore does **not** support ACID or concurrency.

Example:
User A writes:
```python
dbutils.fs.put("/FileStore/test.txt", "A wrote", True)
```
User B writes:
```python
dbutils.fs.put("/FileStore/test.txt", "B wrote", True)
```

Final content:
```
B wrote
```

---

## 12. Practical Exercise — Convert FileStore CSV to Delta Table
```python
df = spark.read.csv("dbfs:/FileStore/tables/orders.csv", header=True, inferSchema=True)

df.write.format("delta").saveAsTable("sales.orders_delta")
```

### What Happens Internally
1. Reads CSV from FileStore  
2. Creates Delta table in Hive Metastore  
3. Writes data to warehouse directory  
4. Generates `_delta_log`  
5. Table appears in Data Explorer  

---

## End of FileStore Topic
