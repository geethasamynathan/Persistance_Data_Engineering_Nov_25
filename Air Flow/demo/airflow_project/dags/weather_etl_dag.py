from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
import requests
import json
import psycopg2

# -------------------------------
# 1. Python Function - Extract Step
# -------------------------------
def extract_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.6&longitude=77.2&current_weather=true"
    response = requests.get(url)
    data = response.json()
    with open("/tmp/weather_raw.json", "w") as f:
        json.dump(data, f)
    print("Weather data extracted successfully:", data)

# -------------------------------
# 2. Python Function - Transform Step
# -------------------------------
def transform_data():
    with open("/tmp/weather_raw.json", "r") as f:
        data = json.load(f)

    # CORRECT KEYS
    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]

    cleaned_data = {"temperature": temp, "windspeed": wind}

    with open("/tmp/weather_clean.json", "w") as f:
        json.dump(cleaned_data, f)

    print("Weather data transformed:", cleaned_data)

# -------------------------------
# 3. Python Function - Load Step (Postgres)
# -------------------------------
def load_to_postgres():
    conn = psycopg2.connect(
        host="postgres",
        dbname="airflow",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    with open("/tmp/weather_clean.json", "r") as f:
        data = json.load(f)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            temperature FLOAT,
            windspeed FLOAT,
            load_time TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        INSERT INTO weather_data (temperature, windspeed)
        VALUES (%s, %s)
    """, (data["temperature"], data["windspeed"]))

    conn.commit()
    cur.close()
    conn.close()

    print("Data loaded into Postgres:", data)

# -------------------------------
# 4. Branch function — success or failure
# -------------------------------
def check_data():
    with open("/tmp/weather_clean.json", "r") as f:
        data = json.load(f)

    print("Branch check:", data)

    if data["temperature"] > 0:
        return "success_task"
    else:
        return "failure_task"

# -------------------------------
# DAG Definition
# -------------------------------
with DAG(
    dag_id="weather_etl_dag",
    description="Real-world ETL pipeline with multiple operators",
    start_date=datetime(2025, 1, 1),
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
        bash_command="echo 'Validating data...' && sleep 2"
    )

    decide = BranchPythonOperator(
        task_id="branch_decision",
        python_callable=check_data
    )

    success_task = EmailOperator(
        task_id="success_task",
        to="geethasamynathan2011@gmail.com",
        subject="Weather ETL Success",
        html_content="<h3>The Weather ETL pipeline ran successfully!</h3>"
    )

    failure_task = EmailOperator(
        task_id="failure_task",
        to="geethasamynathan2011@gmail.com",
        subject="Weather ETL Failure",
        html_content="<h3>The Weather ETL pipeline failed!</h3>"
    )

    end = EmptyOperator(task_id="end")

    start >> extract >> transform >> load >> validate >> decide
    decide >> success_task >> end
    decide >> failure_task >> end
