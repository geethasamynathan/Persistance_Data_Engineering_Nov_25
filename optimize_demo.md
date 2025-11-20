# Databricks OPTIMIZE Demo (20 Small Files → Compacted)

## ✅ STEP 1 — Generate 20 Small Files
```python
from pyspark.sql.functions import *
import random

# Create dummy data
data = []
for i in range(200):
    data.append((
        i,
        random.randint(1, 10),          # product_id
        random.randint(100, 5000),      # amount
        f"2024-01-{random.randint(1, 3):02d}"   # order_date
    ))

df = spark.createDataFrame(data, ["order_id","product_id","amount","order_date"])

# Write into 20 small files
path = "/tmp/optimize_demo"
df.repartition(20).write.format("delta").mode("overwrite").save(path)
```

---

## ✅ STEP 2 — Register Delta Table
```python
spark.sql("""
DROP TABLE IF EXISTS optimize_demo
""")
```

```python
spark.sql(f"""
CREATE TABLE optimize_demo
USING DELTA
LOCATION '{path}'
""")
```

---

## ✅ STEP 3 — Check FILE COUNT (Before OPTIMIZE)
```python
spark.sql("DESCRIBE DETAIL optimize_demo").select("numFiles","sizeInBytes").show()
```

Expected:
```
numFiles: 20
```

---

## ✅ STEP 4 — Run OPTIMIZE
```python
spark.sql("OPTIMIZE optimize_demo")
```

---

## ✅ STEP 5 — Check FILE COUNT (After OPTIMIZE)
```python
spark.sql("DESCRIBE DETAIL optimize_demo").select("numFiles","sizeInBytes").show()
```

Expected:
```
numFiles: 1
```

---

## ⭐ Summary  
Databricks compacted 20 tiny files into 1 large file.  
This improves performance for:
- Reads  
- MERGE  
- UPDATE / DELETE  
- Gold layer analytics  
- File skipping  
