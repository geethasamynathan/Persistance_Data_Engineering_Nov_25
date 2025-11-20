
# ⭐ Data Quality & Validation Frameworks in Databricks

## 📘 What is Data Quality?

Data Quality ensures that data entering the Databricks Lakehouse is:

✔ Accurate  
✔ Complete  
✔ Consistent  
✔ Valid  
✔ Reliable  
✔ Fresh  

Databricks provides multiple built-in and external frameworks to guarantee high-quality data pipelines across **Bronze → Silver → Gold** layers.

---

# ⭐ Why Data Quality Matters

Real-world data often contains:

- Missing values  
- Incorrect types  
- Duplicates  
- Invalid ranges  
- Schema drift  
- Corrupted files  

Without validation → Bad data enters Silver/Gold layers → Wrong dashboards → Wrong business decisions.

---

# ⭐ Data Quality & Validation Frameworks in Databricks

There are **4 major approaches**:

---

# 🟣 1. Delta Lake Data Quality (Built-In)

Delta Lake provides:

### ✔ Schema Enforcement  
Rejects data that doesn’t match expected schema.

```python
df.write.format("delta").save(path)
```

### ✔ Schema Evolution  
Allows adding new columns safely.

```python
.option("mergeSchema", "true")
```

### ✔ Delta Constraints  
Enforce rules at the table level.

```sql
ALTER TABLE sales ADD CONSTRAINT valid_qty CHECK (quantity > 0);
```

---

# 🟣 2. Delta Live Tables Expectations (Enterprise/Trial)

Delta Live Tables (DLT) provides:

✔ Built-in validation  
✔ Rule tagging  
✔ Automatic bad record tracking  
✔ Quality metrics  
✔ Pipeline monitoring  

Example:

```python
@dlt.expect("valid_quantity", "quantity > 0")
def clean_sales():
    return dlt.read("raw_sales")
```

⚠️ *DLT is not available in Community Edition.*

---

# 🟣 3. PySpark-Based Validation (Works in Community Edition)

Use PySpark logic to validate:

### Example:

```python
from pyspark.sql.functions import col

clean_df = raw_df     .filter(col("quantity") > 0)     .filter(col("price") > 0)     .filter(col("customer_id").isNotNull())
```

Capture bad rows:

```python
invalid_df = raw_df.filter(
    (col("quantity") <= 0) |
    (col("price") <= 0)
)
```

---

# 🟣 4. Great Expectations (Open Source Framework)

Great Expectations integrates with Databricks for powerful validations.

Example:

```python
import great_expectations as gx
df_ge = gx.from_pandas(df.toPandas())

df_ge.expect_column_values_to_not_be_null("customer_id")
df_ge.expect_column_values_to_be_between("quantity", 1, 1000)
```

---

# ⭐ Types of Data Quality Checks

| Type | Examples |
|------|----------|
| **Completeness** | Null checks |
| **Validity** | Range checks |
| **Accuracy** | Negative numbers invalid |
| **Uniqueness** | Duplicate order IDs |
| **Freshness** | Timestamp checks |
| **Consistency** | Foreign key lookups |
| **Schema Rules** | Type enforcement |

---

# ⭐ Data Quality in the Medallion Architecture

## 🥉 Bronze Layer
✔ Preserve raw data  
✔ Basic ingestion checks  
✔ Capture corrupted rows  

## 🥈 Silver Layer
✔ Deduplicate  
✔ Validate values  
✔ Join reference data  
✔ Type casting  
✔ Business rules  

## 🥇 Gold Layer
✔ Validated KPIs  
✔ Financial checks  
✔ Dashboard-ready metrics  

---

# ⭐ Real-World Example: Retail Pipeline

### Bronze → Silver Validation Rules
- quantity > 0  
- price > 0  
- order_id must be numeric  
- product_id must exist  

### PySpark Example

```python
good_df = sales_df.filter(
    (col("order_id").isNotNull()) &
    (col("quantity") > 0) &
    (col("price") > 0)
)

bad_df = sales_df.filter(
    (col("order_id").isNull()) |
    (col("quantity") <= 0) |
    (col("price") <= 0)
)
```

Save valid data:

```python
good_df.write.format("delta").mode("overwrite").save("/dbfs/silver/sales")
```

Save bad data:

```python
bad_df.write.format("delta").mode("append").save("/dbfs/bronze/error_sales")
```

---

# ⭐ Summary

**Data Quality & Validation Frameworks in Databricks ensure that only clean, validated, consistent data moves from Bronze → Silver → Gold through built-in Delta Lake constraints, PySpark validation, DLT expectations, and Great Expectations.**

---

# 🎁 Need More?

I can generate:

✔ HTML version  
✔ DOCX version  
✔ PPTX slides  
✔ Databricks Notebook (.dbc)

Just ask!
