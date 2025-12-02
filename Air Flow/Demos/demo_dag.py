from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator




def mwaa_tutorial():
    return 'I love Amazon managed Apache Airflow'





default_args = {
    'owner': 'tuplespectra',
    'start_date': datetime(2023, 1, 8),
    'email': ['tuplespectra@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG('mwaa_demo_tutorial',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:


        start = DummyOperator(
        task_id ='start_task'
        )


        tutorial = PythonOperator(
        task_id = 'mwaa_tutorial_task',
        python_callable=mwaa_tutorial


        )

        end = DummyOperator(
        task_id ='end_task'
        )



        start >> tutorial >> end