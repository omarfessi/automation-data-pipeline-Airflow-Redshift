from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator

from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
	ui_color = '#358140'

	def __init__(
		self,
		redshift_conn_id='',
		aws_credentials_id='',
		destination_table='',
		s3_bucket='',
		s3_key='',
		format_as_json='',
		*args, **kwargs) : 

		super (StageToRedshiftOperator, self).__init__(*args, **kwargs)
		self.redshift_conn_id=redshift_conn_id
		self.aws_credentials_id=aws_credentials_id
		self.destination_table = destination_table 
		self.s3_bucket=s3_bucket
		self.s3_key=s3_key
		self.format_as_json = format_as_json

	def execute (self, context ):

		aws_hook = AwsHook(self.aws_credentials_id)
		credentials = aws_hook.get_credentials()

		# Instanciate a postgres hook to run sql statement in redshift
		redshift=PostgresHook(postgres_conn_id=self.redshift_conn_id)


		# delete table 
		self.log.info(f"Clearing data from _{self.destination_table}_ in Redshift")
		redshift.run("DELETE FROM {}".format(self.destination_table))

		# copy data from S3 to redshift
		self.log.info(f"Copying_{self.destination_table}_data from S3 to redshift")
		s3_path = ("s3://{}/{}").format(self.s3_bucket, self.s3_key)
		redshift.run(f"COPY {self.destination_table} \
					  FROM '{s3_path}' \
					  ACCESS_KEY_ID '{credentials.access_key}' \
					  SECRET_ACCESS_KEY '{credentials.secret_key}'\
					  FORMAT AS JSON '{self.format_as_json}'  ")
		record=redshift.get_records(f"COUNT (*) FROM {self.destination_table}")
		self.log.info(f"Copying_{self.destination_table}_ data is done with success with {record[0][0]} records")



