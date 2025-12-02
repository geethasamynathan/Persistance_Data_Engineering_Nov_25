from airflow import DAG
from datetime import datetime
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator

with DAG(
    "run_databricks_notebook",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
):
    run_nb = DatabricksRunNowOperator(
        task_id="run_bronze_to_silver",
        databricks_conn_id="databricks_default",
        notebook_params={},
        job_id=971761942996822  # your Databricks Job ID
    )
