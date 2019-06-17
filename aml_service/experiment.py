from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core.authentication import AzureCliAuthentication
import os

auth_cli = AzureCliAuthentication()

def get_Experiment():
    ws = Workspace.from_config(path="aml_config/config.json", auth=auth_cli)
    script_folder = '.'
    experiment_name = 'classifier-demo'
    exp = Experiment(worksace=ws, name=experiment_name)
    print(exp.name, exp.workpsace.name, sep='\t')
    return exp

if __name__ == "__main__":
    exp = get_Experiment()
