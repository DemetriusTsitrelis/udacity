from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'depends_on_past': False,  # The DAG does not have dependencies on past runs
    'start_date': datetime(2018, 11, 1),
    'end_date': datetime(2018, 11, 30),
    'retries': 3,  # On failure, the task are retried 3 times
    'retry_delay': timedelta(minutes=5),  # Retries happen every 5 minutes
    'catchup': False,  # Catchup is turned off
    'email_on_retry': False  # Do not email on retry
}

with DAG('etl_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          max_active_runs=1
        ) as dag:

    start_operator = DummyOperator(task_id='Begin_execution')

    copy_sql = """
        COPY public.staging_events
        FROM 's3://udacity-dend/log_data/{year}/{month:02d}/{year}-{month:02d}-{day:02d}-events.json'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON 's3://udacity-dend/log_json_path.json'
        TIMEFORMAT 'epochmillisecs'
        REGION 'us-west-2'
    """
    
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="public.staging_events",
        copy_sql=copy_sql,
        provide_context=True
    )

    copy_sql = """
        COPY public.staging_songs
        FROM 's3://udacity-dend/song_data/'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON 'auto'
        REGION 'us-west-2'
    """
    
    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="public.staging_songs",
        copy_sql=copy_sql,
        provide_context=True
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id="redshift",
        table="public.songplays",
        sql=SqlQueries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id="redshift",
        table="public.users",
        sql=SqlQueries.user_table_insert
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id="redshift",
        table="public.songs",
        sql=SqlQueries.song_table_insert
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id="redshift",
        table="public.artists",
        sql=SqlQueries.artist_table_insert
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id="redshift",
        table='public."time"',
        sql=SqlQueries.time_table_insert
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id = "redshift",
        tests_results = [
            ("SELECT COUNT(*) FROM public.staging_events WHERE userid = 0", 0),
            ("SELECT COUNT(*) FROM public.staging_songs WHERE song_id IS NULL", 0),
            ("SELECT COUNT(*) FROM public.songplays WHERE songid IS NULL", 0),
            ("SELECT COUNT(*) FROM public.users WHERE first_name IS NULL", 0),
            ("SELECT COUNT(*) FROM public.songs WHERE title IS NULL", 0),
            ("SELECT COUNT(*) FROM public.artists WHERE name IS NULL", 0),
            ('SELECT COUNT(*) FROM public."time" WHERE weekday IS NULL', 0),
        ]
    )

    end_operator = DummyOperator(task_id='Stop_execution')

    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [
        load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table,
        load_time_dimension_table] >> run_quality_checks >> end_operator
