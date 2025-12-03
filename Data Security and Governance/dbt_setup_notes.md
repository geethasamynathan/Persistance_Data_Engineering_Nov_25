# dbt (Data Build Tool) – Beginner to Advanced Setup Guide  
*A complete Markdown note for Data Engineering with AWS Databricks*

---

## ⭐ What is dbt?

dbt (Data Build Tool) is an open‑source framework that helps data engineers and analysts **transform data using SQL** inside the data warehouse/lakehouse.

dbt helps you:
- Write modular SQL models  
- Build automated pipelines  
- Add tests & documentation  
- Track lineage  
- Use version control (Git)  
- Run transformations on your warehouse (not locally)

Supported warehouses:
- Databricks  
- Snowflake  
- Redshift  
- BigQuery  
- Postgres  

---

## ⭐ Official Links

### 🔗 dbt Website  
https://www.getdbt.com/

### 🔗 Documentation  
https://docs.getgetdbt.com/

### 🔗 dbt Cloud Sign‑up  
https://www.getdbt.com/signup/

### 🔗 dbt Core Installation  
https://docs.getdbt.com/docs/core/installation

---

# ⭐ Two Ways to Use dbt

| Method | When to Use |
|--------|-------------|
| **dbt Cloud** | Best for beginners & enterprise; includes scheduler, IDE |
| **dbt Core (CLI)** | Best for engineers who want full control on laptop/server |

---

# ⭐ PART 1 — dbt Cloud Setup (Recommended)

## ✅ Step 1: Sign Up  
Create a free account:  
https://www.getdbt.com/signup/

## ✅ Step 2: Connect Your Warehouse  
dbt Cloud works with:
- Databricks
- Snowflake
- BigQuery
- Redshift

### Example: Databricks Connection  
You need:
- Databricks SQL endpoint  
- Hostname  
- HTTP Path  
- Personal Access Token  
- Catalog  
- Schema  

Enter details into dbt Cloud connection setup.

---

## ✅ Step 3: Create a New Project  
Select:
- “Start from Scratch”  
- Choose your warehouse  
- Let dbt auto‑generate sample project structure  

---

## ✅ Step 4: Run Your First Model  
dbt generates a sample file:

`models/example/my_first_dbt_model.sql`

Modify:

```sql
select * from {{ source('raw', 'orders') }}
```

Run:
- **Build**
- **Run**
- **Test**

---

# ⭐ PART 2 — Setup dbt Core (Local Installation)

## 🔧 Step 1: Install Python  
Recommended: Python 3.10  
```
python --version
```

## 🔧 Step 2: Create a Virtual Environment
```
python -m venv dbt-env
source dbt-env/bin/activate   # Mac/Linux
dbt-env\Scripts\activate    # Windows
```

## 🔧 Step 3: Install dbt Adapter

### Databricks
```
pip install dbt-databricks
```

### Snowflake
```
pip install dbt-snowflake
```

### BigQuery
```
pip install dbt-bigquery
```

### Redshift
```
pip install dbt-redshift
```

---

## 🔧 Step 4: Initialize Project

```
dbt init my_project
```

Follow prompts to configure warehouse.

---

## 🔧 Step 5: Configure profiles.yml

Location:
```
~/.dbt/profiles.yml
```

### Sample (Databricks)

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: databricks
      host: adb-123.45.azuredatabricks.net
      http_path: /sql/1.0/endpoints/xyz
      token: dapi123
      catalog: main
      schema: analytics
      threads: 4
```

---

## 🔧 Step 6: Create Your First dbt Model  

Create file:
`models/customers.sql`

```sql
select
    id,
    name,
    email,
    created_at
from {{ source('raw_layer', 'customers') }}
```

---

## 🔧 Step 7: Run dbt  

```
dbt run
```

## 🔧 Step 8: Test Data  
```
dbt test
```

## 🔧 Step 9: Generate Documentation  
```
dbt docs generate
dbt docs serve
```

You get full lineage graph + documentation UI.

---

# ⭐ dbt Real‑World Workflow

```
Raw → Staging → Intermediate → Mart → BI Layer
```

Example:

```
raw.orders → stg_orders → int_orders → mart_sales
```

dbt handles:
- SQL models  
- Tests  
- Documentation  
- Lineage  
- CI/CD with GitHub or GitLab  

---

# ⭐ Real Industry Use Case (AWS + Databricks + dbt)

### E‑Commerce Sales Analytics Pipeline  
1. Raw CSV/JSON lands in S3  
2. Databricks loads into Bronze/Silver/Gold  
3. dbt models:
   - stg_orders
   - stg_customers
   - int_order_items
   - fct_sales  
4. dbt tests:
   - unique order_id  
   - not null customer_id  
5. dbt docs generate → publish lineage  
6. Power BI connects to Gold layer  

Result: Automated, well‑governed transformation pipeline.

---

# ⭐ Next Steps  
Tell me to generate:

- Folder structure for dbt project  
- Sample dbt SQL models  
- dbt tests  
- dbt project ZIP file  
- W3Schools‑style HTML guide  
- dbt + Databricks + Unity Catalog integration guide  

