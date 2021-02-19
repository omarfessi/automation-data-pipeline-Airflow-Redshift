from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG
from datetime import timedelta
from datetime import datetime 

from airflow.operators import CreateTablesOperator
from airflow.operators import StageToRedshiftOperator
from airflow.operators import LoadFactOperator
from airflow.operators import LoadDimensionOperator

from helpers import SqlQueries
default_args = {
	'owner':'Omar',
	'start_date':datetime(2019,1,12),
	'depends_on_past':False,
	'retries':3,
	'retry_delay':timedelta(minutes=5),
	'email_on_retry':False}

dag=DAG('main_dag', 
		default_args = default_args,
		description  = 'Load and transform data into Redshift using Airflow',
		schedule_interval='0 0 1 * *',
		catchup=False)


start_operator=DummyOperator(task_id='Begin_execution', dag=dag)

create_all_tables=CreateTablesOperator(
	task_id='create_all_tables',
	redshift_conn_id='redshift',
	dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
	task_id='load_stage_events',
	dag=dag,
	redshift_conn_id='redshift',
	aws_credentials_id='aws_credentials',
	s3_bucket='udacity-dend',
	s3_key='log_data',
	destination_table='staging_songs',
	format_as_json='s3://udacity-dend/log_json_path.json')

stage_songs_to_redshift = StageToRedshiftOperator(
	task_id='load_stage_songs',
	dag=dag,
	redshift_conn_id='redshift',
	aws_credentials_id='aws_credentials',
	s3_bucket='udacity-dend',
	s3_key='song_data',
	destination_table='staging_songs',
	format_as_json='auto')

load_songplays_table = LoadFactOperator(
	task_id='load_songplays_fact_table',
	dag=dag,
	dimension_table='songplays',
	redshift_conn_id='redshift',
	delete_before_insert=True,
	sql_stmt=SqlQueries.songplay_table_insert
	)

load_users_table = LoadDimensionOperator(
	task_id='load_users_dim_table',
	dag=dag,
	dimension_table='users',
	redshift_conn_id='redshift',
	delete_before_insert=True,
	sql_stmt=SqlQueries.user_table_insert)


start_operator >> create_all_tables 
create_all_tables >> [stage_events_to_redshift, stage_songs_to_redshift]
[stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
[stage_events_to_redshift, stage_songs_to_redshift] >> load_users_table