from __future__ import print_function

import os
import sys
import time
from builtins import range
from datetime import datetime

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from nasdaq import Nasdaq

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

args = {
    'owner': 'daijunkai',
}

dag = DAG(
    dag_id='get_all_nasdaq',
    default_args=args,
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
)


def get_all_nasdaq(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)
    Nasdaq()._get()


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=get_all_nasdaq,
    dag=dag)

# Generate 10 sleeping tasks, sleeping from 0 to 9 seconds respectively
for i in range(2):
    task = PythonOperator(
        task_id='sleep_for_' + str(i),
        python_callable=get_all_nasdaq,
        op_kwargs={'random_base': float(i) / 10},
        dag=dag)

    task.set_upstream(run_this)
