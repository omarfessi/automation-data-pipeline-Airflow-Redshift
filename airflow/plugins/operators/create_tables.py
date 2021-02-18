from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
import create_sql_statements

class CreateTablesOperator(BaseOperator):
	ui_color='#0D70F7'
	def __init__(self, redshift_conn_id='', *args, **kwargs):
		super(CreateTablesOperator, self).__init__(*args, **kwargs)
		self.redshift_conn_id=redshift_conn_id

	def execute ( self, context):
		redshift=PostgresHook(postgres_conn_id=self.redshift_conn_id)
		for table in create_sql_statements.create_all_tables_statement:
			redshift.run(table) 
