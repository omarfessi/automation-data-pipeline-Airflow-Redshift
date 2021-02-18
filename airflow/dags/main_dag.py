from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG
from datetime import timedelta


default_args = {
	'owner':'Omar',
	'start_date':datetime(2019,1,12),
	'depends_on_past':False,
	'retries':3,
	'retry_delay':timedelta(minutes=5)
}

dag=DAG('main_dag', 
		default_args = default_args,
		description  = 'Load and transform data into Redshift using Airflow',
		schedule_interval='',
		catchup=False)


start_operator=DummyOperator(task_id='Begin_execution', dag=dag)

