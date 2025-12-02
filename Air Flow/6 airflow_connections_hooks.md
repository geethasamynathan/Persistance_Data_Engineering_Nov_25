# Connections and Hooks in Apache Airflow (MWAA-Compatible)

## 1. What is a Connection in Apache Airflow?

A **Connection** in Airflow is a stored configuration containing:
- Host / endpoint
- Port
- User credentials (username/password)
- Authentication tokens
- Extra settings such as regions, JSON configs, schemas
- Connection type (AWS, MySQL, HTTP, etc.)

Airflow uses connections to avoid storing passwords inside Python DAG code.

### Common Connection Examples
| Conn ID          | Type      | Purpose                           |
|------------------|-----------|-----------------------------------|
| `aws_default`    | AWS       | S3, Lambda, Redshift              |
| `mysql_default`  | MySQL     | Connect to MySQL DB               |
| `http_default`   | HTTP      | REST API calls                    |

---

## 2. What is a Hook?

A **Hook** is a Python helper class that:
- Reads the connection from Airflow UI
- Creates a client (e.g., boto3, MySQL, Postgres)
- Provides ready-made methods to interact with external systems

### Examples of Popular Hooks
- `S3Hook` – AWS S3 operations  
- `MySqlHook` – MySQL queries  
- `HttpHook` – REST API calls  
- `RedshiftSQLHook`, `GlueJobHook`, etc.

### Example
```python
hook = S3Hook(aws_conn_id="aws_default")
hook.list_keys(bucket_name="my-bucket")
```

---

## 3. Why Use Connections & Hooks?

### Benefits
- **Security:** No hard-coded passwords in Python code  
- **Reusability:** One connection → used by many DAGs  
- **Maintainability:** Update password only once  
- **Portability:** Same DAG works in Local Airflow and AWS MWAA  
- **Developer friendly:** Hooks reduce boilerplate code  

---

## 4. Using Connections & Hooks in Local Airflow (MWAA-like)

Local Airflow behaves exactly like Amazon MWAA:
- Same UI
- Same DAG structure
- Same connection types
- Same Hooks

So everything you develop locally works 100% in MWAA.

---

## 5. Setup Local Apache Airflow Using Docker

### Step 1 — Create Project Folder
```
airflow_local/
 ├── dags/
 ├── logs/
 └── plugins/
```

### Step 2 — Download Docker Compose File
```
curl -LfO https://airflow.apache.org/docs/apache-airflow/2.8.1/docker-compose.yaml
```

### Step 3 — Initialize Airflow
```
docker compose up airflow-init
```

### Step 4 — Start Airflow
```
docker compose up -d
```

### Step 5 — Open Airflow UI
Visit:  
**http://localhost:8080**

Default login:
- **Username:** airflow  
- **Password:** airflow  

---

## 6. Create a Connection (Local)

Go to:

**Airflow UI → Admin → Connections → + Add**

Example AWS connection:

| Field     | Value |
|-----------|--------|
| Conn ID   | aws_default |
| Type      | Amazon Web Services |
| Access Key | YOUR_KEY |
| Secret Key | YOUR_SECRET |
| Extra     | {"region_name": "ap-south-1"} |

---

## 7. Example DAG Using S3Hook & Connection

Save this file as `dags/example_s3_hook.py`:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def list_s3_objects():
    hook = S3Hook(aws_conn_id="aws_default")
    bucket = "my-demo-bucket"
    keys = hook.list_keys(bucket)
    print("Files:", keys)

with DAG(
    dag_id="example_s3_hook",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="list_s3_files",
        python_callable=list_s3_objects
    )
```

---

## 8. MySQL Hook Example

Create a connection named: **my_mysql_conn**

Then use this DAG:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime

def query_mysql():
    mysql = MySqlHook(mysql_conn_id="my_mysql_conn")
    df = mysql.get_pandas_df("SELECT * FROM customers LIMIT 5;")
    print(df)

with DAG(
    "mysql_hook_example",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="read_mysql_data",
        python_callable=query_mysql
    )
```

---

## 9. Local Airflow vs MWAA — Are They Free?

| Environment | Free? | Notes |
|-------------|-------|--------|
| Local Airflow (Docker) | ✅ Yes | Completely free |
| AWS MWAA | ❌ No | Not included in AWS Free Tier |

---

## 10. Summary

- **Connections = saved credentials**
- **Hooks = Python helpers that use those credentials**
- Local Airflow = MWAA equivalent for development
- Hooks simplify AWS, Database, API operations
- All code written locally runs in MWAA without changes

---

Let me know if you want:
- A full ETL pipeline example  
- W3Schools-style HTML version  
- MWAA deployment-ready folder  
- Dynamic + parameterized DAG examples  
