from airflow import DAG
from airflow.decorators import task
from datetime import datetime

@task
def run_sales_etl(store, process_date):
    print(f"ETL running for {store} on {process_date}")

with DAG(
    dag_id="retail_task_mapped_etl",
    start_date=datetime(2025,1,1),
    schedule=None
) as dag:

    selected_stores = "{{ dag_run.conf['stores'] }}"
    process_date = "{{ dag_run.conf['process_date'] }}"

    run_sales_etl.expand(
        store=selected_stores,
        process_date=process_date
    )
