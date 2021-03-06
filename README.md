## Infrastructure as Code to configure the Redshift Cluster
There are several ways to manage clusters. If you prefer a more interactive way of managing clusters, you can use the Amazon Redshift console or the AWS Command Line Interface (AWS CLI). If you are an application developer, you can use the Amazon Redshift Query API or the AWS Software Development Kit (SDK) libraries to manage clusters programmatically. In my case I used the AWS SDK Python Library.
##### Create IAM user:
- Open up your AWS Management Console.
- Under AWS services/Security, Identity & compliance choose IAM.
- On the Dashboard in the left, under Access management choose Users
- Click on Add user, fill in the user name and Select AWS access type as programmatic access.
- Click on "Attach existing policies directly", check "AdministratorAccess" and Click on Next:tags
- Choose not to add tags and hit Next:Review
- Finally click on Create use and download your credentials and put it into a safe place 
- Copy&Paste KEY and SECRET into redshift_configuration.cfg ( which I left it blank for you and please do not publicly expose your credentials)

##### Open IaC.ipynb:
This notebook enables to set the infrastructure on AWS:
- Reads the `Redshift_configuration.cfg` which contains your IAM credentials and cluster configuration.
- Creates IAM, Redshift clients
- Creates an IAM role to allow Redshift clusters to call AWS services on your behalf.
- Launches the Redshift Cluster with the following config:
```
{
CLUSTER_IDENTIFIER  = data-modeling-cloud
CLUSTER_TYPE        = multi-node
NUM_NODES           = 4
NODE_TYPE           = dc2.large
}
```
- !!! Do not to clean up the AWS resources in the buttom of the notebook 
- You may encounter inbound rules issues when using `psycopg2` to create connexion with Redshift, If so make sure to add a new inbound rule of type Redshift, port range 5439, and your IP adress as source.
## Docker image for Airflow dependencies 
As Airflow continues to develop and becomes hard to keep its versions and dependencies stable, I choosed not to install Airflow, rather I use a Docker version of it to wrap up all its dependencies and make Aiflow works on every OS without the need to install any extra modules. all the requirements are listed within `requirements.txt` file which will be copied and installed in your docker container. 
For this part of the work ( Docker virtualisation of Airflow environment ) I used this [amazing work](https://github.com/marshall7m/data-engineering-capstone).

To launch Airflow UI and run DAG:
- Launch Docker
- Change to airflow directory from within repo: `cd airflow`
- Build Docker images: `docker build -t my-airflow .`
- Compose Docker Container: `docker-compose up`
- Go to http://localhost:8080/ on your web browser
- Toggle DAG to ON
    
## Repo Directories and Files Dictionary
`airflow/dags/`:  Dag file that glues together the data pipeline ( `main_dag.py` ) 

`airflow/plugins/operators/`: Custom built operators and operator queries used for ETL pipeline 

`airflow/plugins/operators/create_tables.py`: Custom operator to create tables in Redshift

`airflow/plugins/operators/create_sql_statements.py`: Create table statements used in ( `airflow/plugins/operators/create_tables.py`)

`airflow/plugins/operators/stage_redshift.py`: Custom operator to load staging tables in Redshift

`airflow/config/airflow.cfg` : Airflow configuration file

`airflow/scripts/entrypoint.sh`: Initializes Airflow connections, webserver, and scheduler.

`airflow/docker-compose.yml`: Creates Docker container for Postgres and Airflow webserver

`airflow/Dockerfile`: Builds Docker image with needed python packages and configuration files

`IaC.ipynb`: IaC (infrastructure as code) notebook for Redshift cluster management

## Project Execution Steps
1) Open the IaC.ipynb and execute the cells until you have a cluster ready
2) Go back to how to launch Airflow UI and before you toggle DAG to ON create Airflow connexion under Admin : 
* Conn Id : `redshift`
* Conn Type : `Postgres`
* Host : ( the endpoint you get from the jupyter notebook )
* Schema : my-database ( look at the Redshift_configuration.cfg)
* Login : 
* Password : 
* Port : 5439
3) Create a new connexion to access AWS S3 when copying data from S3 to Redshift : 
* Conn Id : `aws_credentials`
* Conn Type : `Amazon Web Services`




