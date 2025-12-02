# Real-World Airflow DAG Example  
### Daily Weather ETL Pipeline with Multiple Operators

---

## 1. Business Scenario  

A company needs a scheduled **Daily Weather ETL pipeline**:

1. Extract weather data from API  
2. Transform into structured JSON  
3. Load into PostgreSQL  
4. Validate load  
5. Branch workflow based on temperature  
6. Send success/failure email  

This is a real Data Engineering pipeline.

---

## 2. Full DAG Code — `weather_etl_dag.py`

```python
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
import requests
import json
import psycopg2

def extract_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.2&current_weather=true"
    response = requests.get(url)
    data = response.json()
    with open("/tmp/weather_raw.json", "w") as f:
        json.dump(data, f)

def transform_data():
    with open("/tmp/weather_raw.json", "r") as f:
        data = json.load(f)
    cleaned = {
        "temperature": data["current_weather"]["temperature"],
        "windspeed": data["current_weather"]["windspeed"]
    }
    with open("/tmp/weather_clean.json", "w") as f:
        json.dump(cleaned, f)

def load_to_postgres():
    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_data(
            id SERIAL PRIMARY KEY,
            temperature FLOAT,
            windspeed FLOAT,
            load_time TIMESTAMP DEFAULT NOW()
        );
    """)

    with open("/tmp/weather_clean.json", "r") as f:
        data = json.load(f)

    cur.execute(
        "INSERT INTO weather_data (temperature, windspeed) VALUES (%s, %s)",
        (data["temperature"], data["windspeed"])
    )

    conn.commit()
    cur.close()
    conn.close()

def check_data():
    with open("/tmp/weather_clean.json", "r") as f:
        data = json.load(f)
    if data["temperature"] > 0:
        return "success_task"
    return "failure_task"

with DAG(
    dag_id="weather_etl_dag",
    description="Real ETL pipeline with multiple operators",
    start_date=datetime(2025,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    start = EmptyOperator(task_id="start")

    extract = PythonOperator(
        task_id="extract_weather_data",
        python_callable=extract_weather_data
    )

    transform = PythonOperator(
        task_id="transform_weather_data",
        python_callable=transform_data
    )

    load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres
    )

    validate = BashOperator(
        task_id="validate_load",
        bash_command="echo 'Validating...' && sleep 2"
    )

    branch = BranchPythonOperator(
        task_id="branch_decision",
        python_callable=check_data
    )

    success_task = EmailOperator(
        task_id="success_task",
        to="admin@example.com",
        subject="ETL Success",
        html_content="<h3>Weather ETL succeeded</h3>"
    )

    failure_task = EmailOperator(
        task_id="failure_task",
        to="admin@example.com",
        subject="ETL Failure",
        html_content="<h3>Weather ETL failed</h3>"
    )

    end = EmptyOperator(task_id="end")

    start >> extract >> transform >> load >> validate >> branch
    branch >> success_task >> end
    branch >> failure_task >> end
```

---

## 3. Operators Explained

| Operator | Purpose |
|----------|---------|
| **PythonOperator** | Runs Python ETL steps |
| **BranchPythonOperator** | Conditional routing |
| **BashOperator** | Validates using shell |
| **EmailOperator** | Sends alerts |
| **EmptyOperator** | Start/End markers |

---

## 4. DAG Flow Diagram

```
start
  |
extract_weather_data
  |
transform_weather_data
  |
load_to_postgres
  |
validate_load
  |
branch_decision → success_task → end
               ↘ failure_task → end
```

---

## 5. Where to Save The DAG File

Save inside your Airflow project:

```
airflow_project/dags/weather_etl_dag.py
```

---

## 6. View DAG in Airflow UI

1. Start Airflow  
```
docker compose up
```

2. Open in browser  
```
http://localhost:8081
```

3. Search: **weather_etl_dag**  
4. Turn toggle **ON**  
5. Click **Trigger DAG**  
6. Check Graph View → Logs  

---

## End of Real-World ETL DAG Tutorial
