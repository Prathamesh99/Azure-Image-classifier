from azureml.core import Workspace
import azureml
import os, json, sys
from azureml.core.authentication import AzureCliAuthentication

print("SDK Version: ", azureml.core.VERSION)

auth_cli = AzureCliAuthentication()

ws = Workspace.from_config(path="aml_config/config.json", auth=auth_cli)
print(ws.name, ws.location, ws.resource_group, ws.location, sep = '\t')
