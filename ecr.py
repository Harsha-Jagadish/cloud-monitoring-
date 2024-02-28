import boto3

# Create a repository using the ECR API calls from the AWS SDK BOTO for python
#Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/client/create_repository.html

# Create client ecr 
ecr_client=boto3.client('ecr', region_name='us-east-1')

repository_name = "my_monitoring_app_image"
response = ecr_client.create_repository(repositoryName=repository_name)

# lets get the repo uri which we will use when setting up the eks client 
repository_uri = response ['repository']['repositoryUri']
print(repository_uri)

# Once we have the ecr repository uri go over the aws console to check if it has been created to verify 
# Now we need to upload our docker image to the repository
# Follow the push commands provided in the ecr repository
# make sure to add the required permissions/policies to the IAM user to allow login access and uploading the image
# Comeplete list of permissions in JSON File

# Once we have pushed the image to the repository
# We create a EKS cluster on the AWS console and connect to a default VPC and subnets (create a EKS role with permissions)
# We need to ensure that the security group configuration is avaible for the port we are using in our application image (5000)
# Create EKS cluster and add node group but first create a EC2 role for your node group to allow access for container registry
# Once node group is created lets move on to the Kubernetes Service 