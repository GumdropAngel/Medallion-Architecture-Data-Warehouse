from airflow import DAG
#menggunakan path import terbaru sesuai warning Airflow
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

#pengaturan default DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#membuat DAG (mengganti schedule_interval menjadi schedule)
with DAG('medallion_architecture_etl', 
         default_args=default_args, 
         schedule='@daily', 
         catchup=False) as dag:

    task_bronze = BashOperator(
        task_id='extract_load_bronze',
        bash_command='python3 /opt/airflow/dags/1_bronze.py'
    )

    task_silver = BashOperator(
        task_id='transform_cleanse_silver',
        bash_command='python3 /opt/airflow/dags/2_silver.py'
    )

    task_gold = BashOperator(
        task_id='build_star_schema_gold',
        bash_command='python3 /opt/airflow/dags/3_gold.py'
    )

    task_datamart = BashOperator(
        task_id='build_view_datamart',
        bash_command='python3 /opt/airflow/dags/4_datamart.py'
    )

    #mengatur urutan eksekusi
    task_bronze >> task_silver >> task_gold >> task_datamart