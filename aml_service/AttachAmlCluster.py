import azureml.core
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.compute_target import ComputeTargetException
import os, json
from azureml.core.compute import RemoteCompute
from azureml.core.conda_dependencies import CondaDependencies


auth_cli = AzureCliAuthentication()

ws = Workspace.from_config(path = "aml_config/config.json", auth = auth_cli)

#Creating cluster
compute_name = os.environ.get("AML_COMPUTE_CLUSTER_NAME", "Mytarget")
compute_min_nodes = os.environ.get("AML_COMPUTE_CLUSTER_MIN_NODES", 0)
compute_max_nodes = os.environ.get("AML_COMPUTE_CLUSTER_MAX_NODES", 1) # Sanket reduced it to 1 from 3
vm_size = os.environ.get("AML_COMPUTE_CLUSTER_SKU", "STANDARD_D2_V2") # Because STANDARD_NC6 is not available

print('creating a new compute target...')
provisioning_config = AmlCompute.provisioning_configuration(vm_size = vm_size, min_nodes = compute_min_nodes, max_nodes = compute_max_nodes)

cpu_cluster = ComputeTarget.create(ws, compute_name, provisioning_config)

security_build = {}
security_build["compute name"] = compute_name
security_build["min nodes"] = compute_min_nodes
security_build["max nodes"] = compute_max_nodes

with open("aml_config/security_build.json", "w") as outfile:
    json.dump(security_build, outfile)
