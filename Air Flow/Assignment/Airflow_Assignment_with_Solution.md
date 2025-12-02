# Real-World Airflow Assignment  
### Weather Data ETL Pipeline (With Complete Solution)

---

## 📌 BUSINESS PROBLEM

The analytics team at **ClimateSense Pvt Ltd** needs daily weather insights for dashboards.  
They want an automated Airflow pipeline that:

1. Extracts weather data from an API  
2. Transforms JSON into clean format  
3. Loads data into PostgreSQL  
4. Validates the load  
5. Branches based on conditions  
6. Sends success/failure notifications  

---

# 🎯 ASSIGNMENT TASKS

## Task 1 — Create DAG: `weather_etl_assignment`
- Schedule: `@daily`
- `catchup=False`
- Add description

---

## Task 2 — Extract API Weather Data
Call:

```
https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.2&current_weather=true
```

Save to:

```
/tmp/assignment_weather_raw.json
```

---

## Task 3 — Transform Step
Extract:
- temperature  
- windspeed  

Save cleaned file to:

```
/tmp/assignment_weather_clean.json
```

---

## Task 4 — Load Step (Postgres)
Table: **weather_assignment**

---

## Task 5 — Validation
Use BashOperator:

```
test -f /tmp/assignment_weather_clean.json
```

---

## Task 6 — Branching
- If temperature > 0 → success email  
- Else → failure email  

---

## Task 7 — Email Notification
Send to:

```
data-team@example.com
```

---

## Task 8 — DAG Flow Diagram

```
start
  ↓
extract
  ↓
transform
  ↓
load
  ↓
validate
  ↓
check_condition  → success_email → end
                 ↘ failure_email → end
```

---

# ⭐ SOLUTION — Full DAG Code

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

def extract_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.2&current_weather=true"
    response = requests.get(url)
    data = response.json()
    with open("/tmp/assignment_weather_raw.json", "w") as f:
        json.dump(data, f)

def transform_weather():
    with open("/tmp/assignment_weather_raw.json", "r") as f:
        data = json.load(f)
    cleaned = {
        "temperature": data["current_weather"]["temperature"],
        "windspeed": data["current_weather"]["windspeed"]
    }
    with open("/tmp/assignment_weather_clean.json", "w") as f:
        json.dump(cleaned, f)

def load_to_db():
    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_assignment (
            id SERIAL PRIMARY KEY,
            temperature FLOAT,
            windspeed FLOAT,
            load_time TIMESTAMP DEFAULT NOW()
        );
    """)

    with open("/tmp/assignment_weather_clean.json", "r") as f:
        data = json.load(f)

    cur.execute(
        "INSERT INTO weather_assignment (temperature, windspeed) VALUES (%s, %s)",
        (data["temperature"], data["windspeed"])
    )

    conn.commit()
    cur.close()
    conn.close()

def check_condition():
    with open("/tmp/assignment_weather_clean.json", "r") as f:
        data = json.load(f)
    if data["temperature"] > 0:
        return "success_email"
    return "failure_email"

with DAG(
    dag_id="weather_etl_assignment",
    description="Assignment: Weather ETL Pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    start = EmptyOperator(task_id="start")

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_weather
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_weather
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_to_db
    )

    validate = BashOperator(
        task_id="validate",
        bash_command="test -f /tmp/assignment_weather_clean.json"
    )

    check_condition = BranchPythonOperator(
        task_id="check_condition",
        python_callable=check_condition
    )

    success_email = EmailOperator(
        task_id="success_email",
        to="data-team@example.com",
        subject="Weather ETL Success",
        html_content="<h3>Pipeline succeeded!</h3>"
    )

    failure_email = EmailOperator(
        task_id="failure_email",
        to="data-team@example.com",
        subject="Weather ETL Failed",
        html_content="<h3>Pipeline failed!</h3>"
    )

    end = EmptyOperator(task_id="end")

    start >> extract >> transform >> load >> validate >> check_condition
    check_condition >> success_email >> end
    check_condition >> failure_email >> end
```

---

# 🎉 END OF ASSIGNMENT + SOLUTION
You are ready to run this pipeline in Airflow.

