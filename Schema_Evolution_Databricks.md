
# ⭐ Schema Evolution in Databricks (Delta Lake)

## 📘 What is Schema Evolution?

Schema Evolution refers to Delta Lake’s ability to **automatically adjust the table schema** when new columns or structural changes appear in incoming data.

It ensures your pipelines do NOT fail when:
- New columns are added
- Column order changes
- Nested fields expand
- Upstream systems evolve

---

## ⭐ Why Schema Evolution is Needed

Real-world data changes frequently:

### ✔ API updates introduce new fields  
### ✔ IoT devices send new attributes  
### ✔ Product catalog adds new metadata  
### ✔ CRM systems change structure  

Without schema evolution → ETL breaks.

Delta Lake prevents this by allowing schema changes safely.

---

## ⭐ Schema Enforcement vs Schema Evolution

| Feature | Meaning |
|--------|---------|
| **Schema Enforcement** | Reject mismatched schemas |
| **Schema Evolution** | Allow safe schema adjustments |

Delta uses both:
- Enforcement → protects correctness  
- Evolution → supports flexibility  

---

# 🧪 Practical Example (Databricks Community Edition)

## 📘 Step 1 — Create original Delta table

```python
data1 = [
    (1, "Ram", 50000),
    (2, "Sita", 60000)
]

df1 = spark.createDataFrame(data1, ["id", "name", "salary"])

df1.write.format("delta").mode("overwrite").save("/dbfs/tmp/employees_schema")
```

---

## 📘 Step 2 — New data arrives with new column

```python
data2 = [
    (1, "Ram", 50000, "IT"),
    (2, "Sita", 60000, "HR")
]

df2 = spark.createDataFrame(data2, ["id", "name", "salary", "department"])
```

Writing normally will fail with a schema mismatch.

---

## 📘 Step 3 — Enable Schema Evolution

### ✔ PySpark

```python
df2.write   .option("mergeSchema", "true")   .format("delta")   .mode("append")   .save("/dbfs/tmp/employees_schema")
```

### ✔ SQL

```sql
ALTER TABLE delta.`/dbfs/tmp/employees_schema`
SET TBLPROPERTIES ('delta.mergeSchema' = 'true');
```

---

## 📘 Step 4 — Read and verify

```python
display(spark.read.format("delta").load("/dbfs/tmp/employees_schema"))
```

Output now includes:

| id | name | salary | department |
|----|------|--------|------------|
| 1 | Ram | 50000 | IT |
| 2 | Sita | 60000 | HR |

---

# ⭐ Where Schema Evolution Is Useful

### ✔ IoT data streams  
### ✔ API ingestion  
### ✔ E-commerce product catalogs  
### ✔ CRM/ERP systems  
### ✔ Slowly evolving enterprise schemas  

---

# ⭐ When NOT to Use Schema Evolution

❌ Banking or regulated environments  
❌ When schema must be tightly controlled  
❌ When incoming data may be messy  

Use **schema enforcement only** in such cases.

---

# ⭐ Summary

Schema Evolution in Delta Lake allows safe and flexible schema updates—including new columns—without breaking pipelines, while still maintaining data quality.

---

# 🎁 Need HTML / Word / PPT?

Tell me:
- **“export to HTML”**
- **“export to DOCX”**
- **“export to PPTX”**
