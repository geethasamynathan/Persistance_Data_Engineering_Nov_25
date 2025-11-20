
# ⭐ Databricks Medallion Architecture – Real-World End-to-End Project (Community Edition)

This document provides a complete, real-world **Retail Sales Analytics Pipeline** implemented fully in **Databricks Community Edition** using the **Medallion Architecture**:

✔ Bronze (Raw Ingestion)  
✔ Silver (Cleaning, Validation, Enrichment)  
✔ Gold (Business Aggregations)  
✔ Cross-Layer Considerations  
✔ Project Presentation  

---

# 📌 1. Medallion Architecture Overview

The **Medallion Architecture** organizes data into incremental quality layers:

| Layer | Purpose | Example Activities |
|------|---------|--------------------|
| **Bronze** | Raw ingestion | Load CSV/JSON/Parquet as-is |
| **Silver** | Cleaning and transformation | Remove nulls, validate schema, join lookup tables |
| **Gold** | Business-level marts | Revenue KPIs, aggregations, dashboards |

This structure improves:
- Data quality  
- Reprocessability  
- Scalability  
- BI readiness  

---

# 🥉 2. Bronze Layer – Raw Ingestion

## ✔ Objective
Bring raw data into Delta format *without modifying it*.

## ✔ Why?
- Maintain original source of truth  
- Help reprocessing  
- Provide audit history  

---

## 🔥 Step 1: Generate Sample Raw Data

```python
raw_sales = [
    ("1001", "C001", "P001", "2024-01-15", 2, 199.50),
    ("1002", "C002", "P002", "2024-01-15", 1, 399.00),
    ("1003", "C003", "P001", "2024-01-16", 4, 399.00),
    ("1004", "C002", "P003", "2024-01-16", 1, 149.00),
]

raw_products = [
    ("P001", "Dove Shampoo", "Beauty", 199.50),
    ("P002", "Samsung Earbuds", "Electronics", 399.00),
    ("P003", "Dell Mouse", "Electronics", 149.00),
]

raw_customers = [
    ("C001", "Akash", "Delhi"),
    ("C002", "Priya", "Chennai"),
    ("C003", "Ravi", "Mumbai")
]

sales_df = spark.createDataFrame(raw_sales, ["order_id","customer_id","product_id","order_date","quantity","price"])
products_df = spark.createDataFrame(raw_products, ["product_id","product_name","category","unit_price"])
customers_df = spark.createDataFrame(raw_customers, ["customer_id","customer_name","city"])
```

---

## 🔥 Step 2: Save Raw Data to Bronze Delta

```python
sales_df.write.format("delta").mode("overwrite").save("/dbfs/bronze/sales")
products_df.write.format("delta").mode("overwrite").save("/dbfs/bronze/products")
customers_df.write.format("delta").mode("overwrite").save("/dbfs/bronze/customers")
```

---

# 🥈 3. Silver Layer – Cleaning, Validation & Enrichment

## ✔ Objective
Convert raw data to **trusted data** by:
- Deduplicating  
- Validating schema  
- Joining product & customer info  
- Creating new derived columns  

---

## 🔥 Step 3: Read Bronze Tables

```python
bronze_sales = spark.read.format("delta").load("/dbfs/bronze/sales")
bronze_products = spark.read.format("delta").load("/dbfs/bronze/products")
bronze_customers = spark.read.format("delta").load("/dbfs/bronze/customers")
```

---

## 🔥 Step 4: Clean & Join

```python
from pyspark.sql.functions import *

silver_sales = bronze_sales     .dropDuplicates(["order_id"])     .filter("quantity > 0")     .filter("price > 0")     .join(bronze_products, "product_id", "left")     .join(bronze_customers, "customer_id", "left")     .withColumn("total_amount", col("quantity") * col("unit_price"))
```

---

## 🔥 Step 5: Save to Silver Layer

```python
silver_sales.write.format("delta").mode("overwrite").save("/dbfs/silver/sales")
```

---

# 🥇 4. Gold Layer – Business Aggregations

## ✔ Objective
Produce analytics-ready data for:
- Dashboards  
- BI reports  
- Machine learning models  

---

## 🔥 Step 6: Load Silver Table

```python
sales_silver = spark.read.format("delta").load("/dbfs/silver/sales")
```

---

## ⭐ Business KPIs

### 1. Daily Revenue
```python
daily_revenue = sales_silver.groupBy("order_date")     .agg(sum("total_amount").alias("revenue"))
```

### 2. Category Revenue
```python
rev_category = sales_silver.groupBy("category")     .agg(sum("total_amount").alias("category_revenue"))
```

### 3. City Sales
```python
rev_city = sales_silver.groupBy("city")     .agg(sum("total_amount").alias("city_sales"))
```

---

## 🔥 Step 7: Save Gold Delta Tables

```python
daily_revenue.write.format("delta").mode("overwrite").save("/dbfs/gold/daily_revenue")
rev_category.write.format("delta").mode("overwrite").save("/dbfs/gold/rev_category")
rev_city.write.format("delta").mode("overwrite").save("/dbfs/gold/rev_city")
```

---

# 🧠 5. Cross-Layer Considerations

## ✔ Delta Log Versioning
```sql
DESCRIBE HISTORY delta.`/dbfs/silver/sales`;
```

## ✔ Time Travel
```python
spark.read.format("delta").option("versionAsOf", 0).load("/dbfs/silver/sales")
```

## ✔ Optimize Query Performance
```sql
OPTIMIZE delta.`/dbfs/silver/sales`;
```

## ✔ VACUUM for Cleanup
```sql
VACUUM delta.`/dbfs/bronze/sales` RETAIN 168 HOURS;
```

## ✔ Schema Evolution
```python
df.write.option("mergeSchema","true").format("delta").save(path)
```

## ✔ ACID Support
- UPDATE  
- DELETE  
- MERGE  
- INSERT  

Databricks Community Edition supports all Delta operations.

---

# 🎤 6. Project Presentation (Interview Ready)

## 🎯 Project Title  
**Retail Sales Analytics Pipeline using Databricks Medallion Architecture**

## 📝 Business Requirement
Analyze:
- Daily revenue  
- Product performance  
- Category insights  
- Regional sales  

## 🛠 Technical Solution
- Ingest raw → Bronze  
- Clean + join → Silver  
- Aggregate KPIs → Gold  
- Use Delta ACID, schema enforcement, time travel  

## 📊 Outcome
- Clean, trusted, optimized data  
- Fast BI dashboards  
- Reliable financial reporting  

---

# 🎉 End of Document
