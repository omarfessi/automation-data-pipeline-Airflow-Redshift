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
