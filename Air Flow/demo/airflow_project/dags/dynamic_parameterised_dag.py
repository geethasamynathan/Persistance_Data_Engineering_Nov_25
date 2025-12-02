from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.param import Param
from datetime import datetime
import json
import random

# -------------------------------------------------
# 1. BUSINESS LOGIC — Python Function
# -------------------------------------------------
def run_sales_etl(store, process_date):
    print(f"Starting ETL for {store} on {process_date}")

    # Simulated ETL process
    sales = random.randint(1000, 10000)
    print(f"{store} sales for {process_date} = {sales}")

    # Example ETL:
    # 1. Read file: s3://retail/sales/{store}/{process_date}.csv
    # 2. Clean + transform
    # 3. Load into Snowflake / Redshift / PostgreSQL

    return f"ETL completed for {store} on {process_date}"

# -------------------------------------------------
# 2. DAG Definition — Parameterized + Dynamic Tasks
# -------------------------------------------------
with DAG(
    dag_id="retail_store_sales_etl",
    description="Dynamic & Parameterized ETL for Multiple Retail Stores",
    start_date=datetime(2025, 1, 1),
    schedule=None,        # Only trigger manually
    catchup=False,
    params={
        "stores": Param(["store_a", "store_b"], type=["array", "string"]),
        "process_date": Param("2025-12-01", type="string")
    }
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    dynamic_tasks = []

    # Loop through all stores & create tasks dynamically
    for store in ["store_a", "store_b", "store_c"]:
        task = PythonOperator(
            task_id=f"sales_etl_{store}",
            python_callable=run_sales_etl,
            op_kwargs={
                "store": store,
                "process_date": "{{ params.process_date }}"
            }
        )
        start >> task >> end
        dynamic_tasks.append(task)
