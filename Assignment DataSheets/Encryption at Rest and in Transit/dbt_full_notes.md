
# DBT (Data Build Tool) – Complete Notes

## 1. Introduction to DBT
DBT (Data Build Tool) is an open-source framework used to transform data inside data warehouses and lakehouses using SQL. DBT enables analytics engineering by combining SQL with software engineering best practices such as version control, testing, documentation, and CI/CD.

DBT focuses on the **T (Transform)** in **ELT workflows**.

---

## 2. Why DBT is Important

### Key Benefits:
- Modular SQL development  
- Built-in testing for data quality  
- Automated documentation and lineage  
- Git-based version control  
- CI/CD deployment  
- Works with most modern platforms: Databricks, Redshift, Snowflake, BigQuery  
- Supports enterprise ELT workflows

---

## 3. Real-World Use Cases

### Use Case 1: Databricks Lakehouse Transformation
Transform Bronze → Silver → Gold tables using DBT SQL models.

### Use Case 2: Redshift + S3 Analytics Pipeline
Load S3 data into Redshift, use DBT to clean, normalize, and model the data.

### Use Case 3: Data Quality Enforcement
Apply tests for:
- Unique primary keys  
- Not-null constraints  
- Referential integrity  

### Use Case 4: Reusable SQL Logic
Migration of scattered SQL queries into version-controlled DBT projects.

### Use Case 5: Enterprise Metrics Definition
Create reliable KPI tables used across Power BI, Tableau, and Looker.

---

## 4. Transformations in DBT

### 4.1 Models
SQL files inside `models/` folder.

Example:
```sql
select
    id,
    name,
    email
from raw.customers
```

---

### 4.2 Materializations
Defines how DBT builds models.

#### Table
```sql
{{ config(materialized = 'table') }}
```

#### View
```sql
{{ config(materialized = 'view') }}
```

#### Incremental
```sql
{{ config(materialized = 'incremental') }}

select * from raw_events
{% if is_incremental() %}
  where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

---

### 4.3 Tests
Schema tests:
```yaml
version: 2
models:
  - name: customers
    columns:
      - name: id
        tests: 
          - unique
          - not_null
```

Custom tests:
```sql
select * from sales where amount < 0
```

---

### 4.4 Macros
Reusable SQL logic.

```sql
{% macro safe_cast(column, type) %}
    try_cast({{ column }} as {{ type }})
{% endmacro %}
```

---

### 4.5 Documentation
Generate documentation:
```
dbt docs generate
dbt docs serve
```

---

## 5. DBT + Databricks Integration

### 5.1 Install Adapter
```
pip install dbt-databricks
```

---

### 5.2 Configure profiles.yml
```yaml
databricks_profile:
  target: dev
  outputs:
    dev:
      type: databricks
      host: https://<workspace-url>
      http_path: /sql/1.0/warehouses/<warehouse-id>
      token: <databricks-access-token>
      catalog: main
      schema: analytics
```

---

### 5.3 Create DBT Models

#### Bronze:
```sql
select * from raw.sales
```

#### Silver:
```sql
select
    order_id,
    customer_id,
    amount
from {{ ref('bronze_sales') }}
```

#### Gold:
```sql
select
    customer_id,
    sum(amount) as total_sales
from {{ ref('silver_sales') }}
group by customer_id
```

---

### 5.4 Run DBT
```
dbt run
dbt test
dbt docs generate
```

---

## 6. DBT with S3 + Redshift

### Workflow:
1. Raw files stored in S3  
2. COPY command moves data into Redshift staging tables  
3. DBT models transform data into marts (dim/fact tables)  

---

### 6.1 COPY Command Example
```
COPY raw.sales
FROM 's3://bucket/sales/'
IAM_ROLE 'arn:aws:iam::<role>'
FORMAT AS PARQUET;
```

---

### 6.2 DBT Staging Model
```sql
{{ config(materialized = "view") }}

select
    sale_id,
    amount,
    created_at
from raw.sales
```

---

### 6.3 Fact & Dimension Models

#### Dimension:
```sql
select
    id as customer_id,
    name,
    email
from raw.customers
```

#### Fact:
```sql
{{ config(materialized='incremental') }}

select
    s.sale_id,
    s.customer_id,
    s.amount
from stg_sales s
```

---

## 7. Architecture Diagrams (Text Format)

### DBT + Databricks Lakehouse
```
S3/ADLS → Bronze → DBT → Silver → DBT → Gold → BI Tools
```

### DBT + Redshift + S3
```
S3 Raw → Redshift Staging → DBT Transformations → Analytics Marts
```

---

## 8. Summary

DBT is a powerful transformation tool used widely for:
- Modular SQL pipelines  
- Data quality tests  
- Data modeling  
- Lineage and documentation  
- Integration with Databricks, Redshift, Snowflake, BigQuery  

DBT standardizes analytics engineering workflows and enhances data reliability.

---

Generated for ItTechGenie 🚀
