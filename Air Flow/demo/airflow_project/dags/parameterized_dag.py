from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import datetime
import random
import time

# -------------------------------------
# PYTHON FUNCTIONS (SIMULATED ETL)
# -------------------------------------

def extract_transactions(process_date, customer_type):
    print(f"Extracting transactions for Date={process_date}, Type={customer_type}")

    # Simulate extracting from a data source
    count = random.randint(50, 300)
    print(f"Extracted {count} transactions")

    return count


def transform_transactions(**context):
    extracted_count = context['ti'].xcom_pull(task_ids='extract')
    print(f"Transforming {extracted_count} transactions...")

    time.sleep(1)
    cleaned = extracted_count * 0.98  # 2% cleaning loss
    print(f"Cleaned records: {cleaned}")

    return cleaned


def load_transactions(**context):
    cleaned_count = context['ti'].xcom_pull(task_ids='transform')
    print(f"Loading {cleaned_count} cleaned transactions into warehouse...")
    print("Load complete!")

# -----------------------------------------
# PARAMETERIZED DAG DEFINITION
# -----------------------------------------

with DAG(
    dag_id="customer_transactions_etl",
    description="ETL for customer transactions with user-defined parameters",
    start_date=days_ago(1),
    schedule=None,                  # Only manual runs
    catchup=False,

    params={
        "process_date": Param("2025-01-01", type="string"),
        "customer_type": Param("Gold", enum=["Gold", "Silver", "Premium"])
    }
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_transactions,
        op_kwargs={
            "process_date": "{{ params.process_date }}",
            "customer_type": "{{ params.customer_type }}"
        }
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_transactions,
        provide_context=True
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_transactions,
        provide_context=True
    )

    extract >> transform >> load
