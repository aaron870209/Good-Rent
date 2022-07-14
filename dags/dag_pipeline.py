from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
import os
from dotenv import load_dotenv
import datetime
load_dotenv()

with DAG(
    'Good-Rent',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email': [os.getenv('my_email')],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=pendulum.datetime(2021, 1, 1,tz="Asia/Taipei"),
    dagrun_timeout=datetime.timedelta(minutes=1440),
    catchup=False,
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    crawl_591 = BashOperator(
        task_id='crawl_591',
        bash_command='cd /home/kairong0209/Good-Rent/crawler && python3 -u crawler_591.py > 591.log',
        do_xcom_push=False,
        dag=dag
    )

    crawl_lewu = BashOperator(
        task_id='crawl_lewu',
        depends_on_past=False,
        bash_command='cd /home/kairong0209/Good-Rent/crawler && python3 -u crawler_lewu.py > lewu.log',
        do_xcom_push=False,
        dag=dag
    )

    data_cleaning = BashOperator(
        task_id='data_cleaning',
        depends_on_past=False,
        bash_command='cd /home/kairong0209/Good-Rent/data_pipeline && python3 -u data_pipeline.py > data_clean.log',
        do_xcom_push=False,
        dag=dag
    )

    crawl_lat_log = BashOperator(
        task_id='crawl_lat_log',
        depends_on_past=False,
        bash_command='cd /home/kairong0209/Good-Rent/crawler && python3 -u crawl_log_lat.py',
        do_xcom_push=False,
        dag=dag
    )

    calculate_truck = BashOperator(
        task_id='calculate_truck',
        depends_on_past=False,
        bash_command='cd /home/kairong0209/Good-Rent/data_pipeline && python3 -u calculate_distance.py',
        do_xcom_push=False,
        dag=dag
    )

    calculate_school = BashOperator(
        task_id='calculate_school',
        depends_on_past=False,
        bash_command='cd /home/kairong0209/Good-Rent/data_pipeline && python3 -u calculate_school_distance.py',
        do_xcom_push=False,
        dag=dag
    )

    crawl_591 >> crawl_lewu >> data_cleaning >> crawl_lat_log >> [calculate_truck,calculate_school]
