from airflow.models import BaseOperator
class LoadDimensionOperator ( BaseOperator):
	ui_color='#F98866'
	def __init__(self, 
		dimension_table='', 
		redshift_conn_id='',
		delete_before_insert='', 
		sql_stmt='',
		*args, **kwargs):
		super(LoadDimensionOperator, self).__init__(*args, **kwargs)

		self.dimension_table=dimension_table
		self.redshift_conn_id=redshift_conn_id
		self.delete_before_insert=delete_before_insert
		self.sql_stmt=sql_stmt

	def execute (self, context):
		redshift=PostgresHook(postgres_conn_id=self.redshift_conn_id)
		self.log.info(f"LoadDimension {self.dimension_table} is being executed ..")
		if self.delete_before_insert:
			self.log.info(f"delete mode is activated .. deleting {self.dimension_table} table")
			redshift.run(f"DELETE FROM {self.dimension_table}")
		redshift.run(self.sql_stmt)


