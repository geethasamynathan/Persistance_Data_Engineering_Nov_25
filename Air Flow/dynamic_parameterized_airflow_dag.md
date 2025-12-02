# Dynamic & Parameterized DAGs in Apache Airflow  
### Real-World ETL Example + Step-by-Step Explanation

## 1. What Are Dynamic & Parameterized DAGs?

### Dynamic DAG  
A DAG that creates tasks programmatically using loops instead of hardcoding tasks.

### Parameterized DAG  
A DAG that accepts inputs such as store name, date, or table name using Airflow params or DagRun.conf.

---

## 2. Real-World Use Case — Multi-Store ETL

Multiple stores upload sales data:
- store_a
- store_b
- store_c

You want 1 ETL task per store, generated dynamically, and allow reruns for specific stores or dates.

---

## 3. Dynamic + Parameterized DAG — Full Code

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

STORE_LIST = ["store_a", "store_b", "store_c"]

def process_store(store_name, date):
    print(f"Processing data for {store_name} on date: {date}")
    return f"{store_name} processing completed"

with DAG(
    dag_id="dynamic_parameterized_store_etl",
    description="ETL pipeline with dynamic & parameterized tasks",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    params={
        "stores": ["store_a", "store_b"],
        "process_date": "2025-10-10"
    }
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    for store in dag.params["stores"]:
        task = PythonOperator(
            task_id=f"process_{store}",
            python_callable=process_store,
            op_kwargs={
                "store_name": store,
                "date": "{{ params.process_date }}"
            }
        )
        start >> task >> end
```

---

## 4. Triggering the DAG

### From UI
```json
{
  "stores": ["store_c"],
  "process_date": "2025-02-01"
}
```

### Using API
```bash
curl -X POST "http://localhost:8081/api/v1/dags/dynamic_parameterized_store_etl/dagRuns"   -u "airflow:airflow"   -H "Content-Type: application/json"   -d '{"conf":{"stores":["store_a","store_c"],"process_date":"2025-02-10"}}'
```

---

## 5. Execution Flow

For:
```
stores = ["store_a", "store_c"]
date = 2025-10-10
```

Airflow creates:
```
start → process_store_a → end
start → process_store_c → end
```

---

## 6. Enterprise Use Cases

| Industry | Use Case |
|----------|----------|
| E-commerce | Multi-store ETL |
| Banking | Branch-level ETL |
| Logistics | Route/hub ETL |
| Healthcare | Hospital processing |
| Food delivery | Restaurant ingestion |

---

## 7. Summary

- **Dynamic DAGs** scale to 100+ tasks.
- **Parameterized DAGs** allow flexible inputs.
- Combined → Perfect for multi-client ETL pipelines.
