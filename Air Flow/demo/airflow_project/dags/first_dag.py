from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Define a Python function for python operator
def my_python_task():
    print("Hello from Python Operator!")

# DAG definition
with DAG(
    dag_id="my_first_dag",
    description="Simple tutorial DAG",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",   # Run every day
    catchup=False,
) as dag:

    # Task 1: BashOperator
    task1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    # Task 2: BashOperator
    task2 = BashOperator(
        task_id="print_message",
        bash_command="echo 'Airflow DAG executed successfully!'"
    )

    # Task 3: PythonOperator
    task3 = PythonOperator(
        task_id="python_task",
        python_callable=my_python_task
    )

    # Task dependencies
    task1 >> task2 >> task3
