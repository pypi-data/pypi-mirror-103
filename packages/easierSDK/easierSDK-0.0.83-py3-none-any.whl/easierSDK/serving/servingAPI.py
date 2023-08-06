import os
import kubernetes
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import string
import random

from easierSDK.classes.categories import Categories
from easierSDK.serving import easier_serving_config_map
from easierSDK.serving import easier_serving_deployment
from easierSDK.serving import easier_serving_service 
from easierSDK.serving import easier_serving_ingress 

class ServingAPI():
    """Class to control the Serving API of EasierSDK.
    """

    def __init__(self, easier_user, easier_password, minio_client, my_public_repo, my_private_repo):
        """Constructor for the ServingAPI.

        Args:
            minio_client (Minio): Minio client object with user session initialized.
            my_public_repo (str): Name of the public bucket of the user.
            my_private_repo (str): Name of the private bucket of the user.
        """
        self._easier_user = easier_user
        self._easier_password = easier_password
        self.minio_client = minio_client
        self.my_public_repo = my_public_repo
        self.my_private_repo = my_private_repo
        self.namespace = None
        
    def initialize(self, kube_config_path=None):
        if kube_config_path:
            kubernetes.config.load_kube_config(kube_config_path)
            with open(os.path.join(os.path.dirname(__file__), kube_config_path)) as f:
                kubeconfig = yaml.safe_load(f)
                self.namespace = kubeconfig['contexts'][0]['context']['namespace']
        else:
            kubernetes.config.load_kube_config()
            with open(os.path.join(os.path.dirname(__file__), os.environ.get('KUBECONFIG', '~/.kube/config'))) as f:
                kubeconfig = yaml.safe_load(f)
                self.namespace = kubeconfig['contexts'][0]['context']['namespace']

        print("Current context on namespace: " + str(self.namespace))
        
    def id_generator(self, size=16, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def create_model_serving(self, repo_name:str, category:Categories, model_name:str, experimentID:int, base_hostname_url='.easier-ai.eu'):
        """Creates a model serving deployment on the infrastructure.

        Args:
            repo_name (str): name of the repository where the model is
            category (Categories): category of the model
            model_name (str): name of the model
            experimentID (int): version of the model
            namespace ([type], optional): namespace where the deployment will be done. Defaults to None to take user's namespace.

        Returns:
            str: hostname of the deployed model
        """
        
        if isinstance(category, str):
           category = Categories[category.upper()]
        
        # Test if model can be loaded
        from easierSDK.easier import EasierSDK
        easier = EasierSDK(easier_user=self._easier_user, easier_password=self._easier_password)
        easier_model = easier.models.get_model(repo_name=repo_name, category=category, model_name=model_name, experimentID=experimentID)    
        if easier_model.get_model() is None:
            print("ERROR: Could not load model " + str(model_name) +
                    " from repository " + repo_name + " and category " + category.value)
            return None

        if self.namespace is None:
            print("ERROR: No context (namespace) was provided. Please, initialize the platform connection before creating model servings.")
            return None
        namespace = self.namespace  
        
        # Enter a context with an instance of the API kubernetes.client
        with kubernetes.client.ApiClient() as api_client:
            # Create an instance of the API class
            api_instance = kubernetes.client.CoreV1Api(api_client)
            
            random_name = self.id_generator(size=5)
            
            # config_map = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-config_map.yaml")) as f:
            config_map = yaml.safe_load(easier_serving_config_map.config_map)

            config_map['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            config_map['data']['easier_user'] = self._easier_user
            config_map['data']['easier_password'] = self._easier_password
            config_map['data']['repo'] = repo_name
            config_map['data']['category'] = category.value
            config_map['data']['model_name'] = model_name
            config_map['data']['experimentID'] = str(experimentID)
            
            try:
                api_response = api_instance.create_namespaced_config_map(namespace, config_map, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

            # deployment = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-deployment.yaml")) as f:
            deployment = yaml.safe_load(easier_serving_deployment.deployment)
        
            deployment['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['spec']['selector']['matchLabels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['spec']['template']['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            deployment['spec']['containers'][0]['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['spec']['containers'][0]['envFrom'][0]['configMapRef']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
    
            try:
                api_response = api_instance.create_namespaced_pod(namespace, deployment, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)

            # service = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-service.yaml")) as f:
            service = yaml.safe_load(easier_serving_service.service)
        
            service['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            service['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            service['spec']['selector']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name

            try:
                api_response = api_instance.create_namespaced_service(namespace, service, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)
        
            networking_v1_beta1_api = kubernetes.client.NetworkingV1beta1Api()
            hostname = None
            # ingress = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-ingress.yaml")) as f:
            ingress = yaml.safe_load(easier_serving_ingress.ingress)
        
            ingress['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            ingress['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            ingress['spec']['rules'][0]['host'] = model_name + '-' + 'easier-serving' + '-' + self._easier_user.replace('.', '-') + '-' + random_name + base_hostname_url
            ingress['spec']['rules'][0]['http']['paths'][0]['backend']['serviceName'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name

            try:
                api_response = networking_v1_beta1_api.create_namespaced_ingress(namespace, ingress, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_ingress: %s\n" % e)
            
            hostname = ingress['spec']['rules'][0]['host']
            
            if hostname:
                print("Your model will be served shortly in: " + str(hostname))
                print("The identifier for the deployment is: " + random_name)
            else:
                print("There was a problem serving your model")

        return random_name

    def delete_serving(deployment_identifier:str):
        """Deletes the deployment resources of a serving.

        Args:
            hostname (str): hostname given as identifier when a serving was created
        """
        hostname = hostname.split("-")
        if self.namespace is None:
            print("ERROR: No context (namespace) was provided. Please, initialize the platform connection before creating model servings.")
            return None
        namespace = self.namespace  
        
        # Enter a context with an instance of the API kubernetes.client
        with kubernetes.client.ApiClient() as api_client:
            # Create an instance of the API class
            api_instance = kubernetes.client.CoreV1Api(api_client)

            try:
                config_map = yaml.safe_load(easier_serving_config_map.config_map)
            
                config_map['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + deployment_identifier
                api_response = api_instance.delete_namespaced_config_map(deployment, namespace)
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_config_map: %s\n" % e)

            try:
                deployment = yaml.safe_load(easier_serving_deployment.deployment)
            
                deployment['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + deployment_identifier
                api_response = api_instance.delete_namespaced_pod(deployment['metadata']['name'], namespace)
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
            
            try:
                service = yaml.safe_load(easier_serving_service.service)
            
                service['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + deployment_identifier
                api_response = api_instance.delete_namespaced_service(service['metadata']['name'], namespace)
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

            try:
                ingress = yaml.safe_load(easier_serving_ingress.ingress)
            
                ingress['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + deployment_identifier
                
                networking_v1_beta1_api = kubernetes.client.NetworkingV1beta1Api()
                api_response = networking_v1_beta1_api.delete_namespaced_ingress(ingress['metadata']['name'], namespace)
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
    