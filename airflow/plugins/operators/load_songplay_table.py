from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator


class LoadFactOperator (BaseOperator):
	ui_color='#F98866'
	def __init__(self, 
		redshift_conn_id='', 
		sql_stmt='', 
		fact_table='', 
		delete_before_insert='', 
		*args, **kwargs):
		super (LoadFactOperator, self).__init__(*args, **kwargs)
		self.redshift_conn_id=redshift_conn_id
		self.sql_stmt=sql_stmt
		self.delete_before_insert=delete_before_insert
		self.fact_table=fact_table

	def execute (self, context):
		redshift=PostgresHook(postgres_conn_id=self.redshift_conn_id)
		self.log.info(f"LoadFact table is being implemented on {self.fact_table}")

		if self.delete_before_insert : 
			self.log.info(f"Delete before insert mode is ON .. deleting {self.fact_table}")
			redshift.run(f"DELETE FROM {self.fact_table}")
		redshift.run(self.sql_stmt)