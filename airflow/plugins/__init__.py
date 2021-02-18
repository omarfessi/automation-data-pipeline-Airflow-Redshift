from __future__ import division, absolute_import, print_function
from airflow.plugins_manager import AirflowPlugin

import operators


#defining the plugin class 
class ProjectPlugin(AirflowPlugin):
	name = 'project_plugin'
	operators = [operators.CreateTables, operators.StageToRedshiftOperator]
