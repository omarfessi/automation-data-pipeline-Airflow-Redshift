from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
class DataQualityOperator(BaseOperator):
	ui_color='#EE6A8C'
	def __init__(self, redshift_conn_id='',table_names=[], *args, **kwargs):
		super(DataQualityOperator, self).__init__(*args, **kwargs)
		self.redshift_conn_id=redshift_conn_id
		self.table_names=table_names

	def execute(self, context): 
		redshift=PostgresHook(self.redshift_conn_id)
		self.log.info('DataQuality is being executed ..')
		self.log.info('*'*20)

		for table in self.table_names:
			records=redshift.get_records(f"SELECT COUNT (*) FROM {table}")
			self.log.info(f"Begin DataQuality on table {table}")

			if len(records) < 1 or len (records[0]) < 1 : 
				raise ValueError ( f"Data quality check failed, {table} returned no results")
			num_records = records[0][0]
			if num_records < 1 :
				raise ValueError ( f"Data quality check failed, {table} returned 0 rows ")
			self.log.info(f"Data quality on table {table} check passed with {records[0][0]} records")
			self.log.info('$'*10)
		dq_checks=[
		{'table': 'users', 'check_sql':'SELECT COUNT (*) FROM users WHERE user_id is null', 'expected_result':0},
		{'table': 'songs', 'check_sql': 'SELECT COUNT (*) FROM songs WHERE song_id is null', 'expected_result':0}
		]
		for check in dq_checks:
			self.log.info('DataQuality check for Null ids')
			records = redshift.get_records (check ['check_sql'])[0]
			if records[0]!=check['expected_result']:
				raise ValueError (f"DataQuality check failed. {check['table']} contains null in id column")
			self.log.info('DataQuality check for Null ids is negative, Well done !')
