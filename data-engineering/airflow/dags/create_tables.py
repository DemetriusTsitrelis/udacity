from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
}

with DAG('create_tables_dag',
         default_args=default_args,
         description='Create tables in Redshift with Airflow',
         schedule_interval=None,
         template_searchpath='/home/workspace/airflow'
         ) as dag:
    start_operator = DummyOperator(task_id='Begin_execution')

    drop_tables_task = PostgresOperator(
        task_id="Drop_tables",
        sql=[
            'DROP TABLE IF EXISTS public.artists',
            'DROP TABLE IF EXISTS public.songplays',
            'DROP TABLE IF EXISTS public.songs',
            'DROP TABLE IF EXISTS public.staging_events',
            'DROP TABLE IF EXISTS public.staging_songs',
            'DROP TABLE IF EXISTS public."time"',
            'DROP TABLE IF EXISTS public.users'
        ],
        postgres_conn_id="redshift"
    )

    create_tables_task = PostgresOperator(
        task_id="Create_tables",
        sql='create_tables.sql',
        postgres_conn_id="redshift"
    )
        
    end_operator = DummyOperator(task_id='Stop_execution')

    start_operator >> drop_tables_task >> create_tables_task >> end_operator
