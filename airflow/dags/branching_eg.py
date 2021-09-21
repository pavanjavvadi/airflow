from datetime import timedelta


# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
with DAG(
    'branching example',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    def branch_func(ti):
        xcom_value = int(ti.xcom_pull(task_ids='start_task'))
        if xcom_value >= 5:
            return 'continue_task'
        else:
            return 'stop_task'

    start_op = BashOperator(
        task_id='start_task',
        bash_command="echo 5",
        xcom_push=True,
    )

    branch_op = BranchPythonOperator(
        task_id='branch_task',
        python_callable=branch_func,
        dag=dag,
    )

    continue_op = DummyOperator(task_id='continue_task')
    stop_op = DummyOperator(task_id='stop_task')

start_op >> branch_op >> [continue_op, stop_op]
