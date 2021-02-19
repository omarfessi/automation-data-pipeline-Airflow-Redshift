from __future__ import division, absolute_import, print_function
from airflow.plugins_manager import AirflowPlugin

import operators
import helpers


#defining the plugin class 
class ProjectPlugin(AirflowPlugin):
	name = 'project_plugin'
	operators = [operators.CreateTablesOperator, \
	operators.StageToRedshiftOperator, \
	operators.LoadFactOperator, \
	operators.LoadDimensionOperator]
	
	helpers = [helpers.SqlQueries]
