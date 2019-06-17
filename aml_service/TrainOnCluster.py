from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
import json
from azureml.core.authentication import AzureCliAuthentication
import azureml.core
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication

auth_cli = AzureCliAuthentication()

ws = Workspace.from_config(path="aml_config/config.json", auth=auth_cli)

ds = ws.get_default_datastore()
print(ds.datastore_type, ds.account_name, ds.container_name, sep="\n")

ds.upload(src_dir='./dataset', target_path='dataset', overwrite=True, show_progress=True)


experiment_name = "Classifier-demo"
exp = Experiment(workspace=ws, name=experiment_name)
print(exp.name, exp.workspace.name, sep="\n")

with open("aml_config/security_build.json") as f:
    config = json.load(f)

#cluster_target = config["compute_name"]
cluster_target = "Mytarget"
run_config = RunConfiguration()
run_config.target = cluster_target

run_config.environment.python.interpreter_path = "/anaconda/envs/myenv/bin/python"
run_config.environment.python.user_managed_dependencies = True

from azureml.train.estimator import Estimator

script_params = {
    '--data-folder': ds.as_mount()
}

est = Estimator(source_directory="./code/training",
                script_params=script_params,
                compute_target=cluster_target,
                entry_script='train.py',
                conda_packages=['scikit-learn', 'keras', 'tensorflow', 'pillow'])

run = exp.submit(config=est)
run
#    source_directory="./code", script="training/train.py", run_config=run_config
#)
#run = exp.submit(src)

if run.get_status() == "Failed":
    raise Exception(
        "Training on local env failed with following run status: {} and logs: \n {}".format(
            run.get_status(), run.get_details_with_logs()
        )
    )

# Writing the run id to /aml_config/run_id.json
run_id = {}
run_id["run_id"] = run.id
run_id["experiment_name"] = run.experiment.name
with open("aml_config/run_id.json", "w") as outfile:
    json.dump(run_id, outfile)