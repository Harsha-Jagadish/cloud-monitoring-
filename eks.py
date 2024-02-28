# Documentation: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
# Instead of yaml lets use python to define the deployment configuration

#create deployment and service
from kubernetes import client, config

# Add the permissions for the user to eks:describeCluster to allow the client to load the kube config 
# Path to your kubeconfig file
kubeconfig_path = '/Users/harsha/.kube/config'


# Load Kubernetes configuration that we have created on eks using the AWS console and 
config.load_kube_config(config_file=kubeconfig_path)

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment 
# A Deployment provides declarative updates for Pods and ReplicaSets.
# You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. 
# You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments.

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="851725605398.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment using python code instead of doing it in cli using "kubectl apply -f deployement.yaml default"
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service so everyone else outside the cluster can access it
# Documentation: https://kubernetes.io/docs/concepts/services-networking/service/
# No need to implememt load balancer I would love to work on large scale projects that do utilize this to learn more

service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)

# Once you run this script you can montior the kube pods, deployment and service using the following commands
# Pods: kubectl get pods -n default -w
# Deployment: kubectl get deployment -n default 
# Service: kubectl get svc -n default
# More details about pods: kubectl describe pods ${p0d_name} -n default