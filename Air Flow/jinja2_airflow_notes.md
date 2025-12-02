# Jinja2 in Apache Airflow

## 🧩 What is Jinja2 in Airflow?
Jinja2 is a powerful templating engine used in Airflow to generate dynamic values inside DAGs, Operators, SQL scripts, and configurations.

## ✔ Why Use Jinja2?

| Feature | Explanation |
|--------|-------------|
| Dynamic values | Use execution date, next execution date, run id, params, variables, etc. |
| Templated SQL | Insert dynamic dates or variables into SQL queries. |
| Templated operators | Pass dynamic arguments to Python & Bash operators. |
| Access Airflow Variables & Params | `{{ var.value.x }}` or `{{ params.x }}` |
| Reusable pipelines | Create generic, parameterized workflows. |

---

## 🧠 Jinja2 Syntax in Airflow

| Purpose | Syntax |
|--------|--------|
| Print variable | `{{ variable }}` |
| Condition | `{% if condition %} ... {% endif %}` |
| Loop | `{% for x in list %} ... {% endfor %}` |
| Access macros | `{{ ds }}`, `{{ next_ds }}` |
| Access variables | `{{ var.value.key }}` |
| Access params | `{{ params.param_name }}` |

---

## 🔥 Common Airflow Macros

| Macro | Meaning |
|-------|---------|
| `{{ ds }}` | Execution date (YYYY-MM-DD) |
| `{{ ds_nodash }}` | 20240101 |
| `{{ ts }}` | Timestamp |
| `{{ next_ds }}` | Next execution date |
| `{{ prev_ds }}` | Previous execution date |
| `{{ dag_run.run_id }}` | Run identifier |
| `{{ logical_date }}` | Execution datetime |

---

## 🧪 Example 1 — Jinja in BashOperator

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="jinja_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily"
):

    print_date = BashOperator(
        task_id="print_date",
        bash_command="echo Today is {{ ds }} and run id is {{ dag_run.run_id }}"
    )
```

---

## 🧪 Example 2 — Jinja2 in SQL File

**query.sql**
```jinja
SELECT *
FROM sales
WHERE sale_date = '{{ ds }}';
```

Python Operator:
```python
SQLExecuteQueryOperator(
    task_id="run_query",
    conn_id="mysql_conn",
    sql="query.sql"
)
```

---

## 🧪 Example 3 — Using Params with Jinja

```python
PythonOperator(
    task_id="process",
    python_callable=process_data,
    params={"table_name": "orders"},
    op_kwargs={"table": "{{ params.table_name }}"}
)
```

---

## ✨ How to Write Jinja2 Code in Markdown

Use a fenced code block:

````markdown
```jinja
SELECT * FROM orders WHERE order_date = '{{ ds }}';
```
````

### Example with logic

````markdown
```jinja
{% if params.region == "IN" %}
    SELECT * FROM india_sales;
{% else %}
    SELECT * FROM global_sales;
{% endif %}
```
````

### Example with loop

````markdown
```jinja
{% for table in params.table_list %}
    SELECT * FROM {{ table }};
{% endfor %}
```
````

---

## 🎯 Summary
- Jinja2 enables dynamic, parameterized DAGs.
- Works with SQL, BashOperator, PythonOperator, EmailOperator, templates.
- Macros like `ds`, `next_ds`, `dag_run.run_id` help automate date handling.
- Markdown notation uses fenced blocks with `jinja`.

