from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG
from datetime import timedelta
from datetime import datetime 
from airflow.operators import CreateTables


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

create_all_tables=CreateTables(
	task_id='create_all_tables',
	redshift_conn_id='redshift',
	dag=dag)