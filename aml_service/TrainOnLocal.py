from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
import json
from azureml.core.authentication import AzureCliAuthentication

auth_cli = AzureCliAuthentication()

ws = Workspace.from_config(path='aml_config/config.json', auth=auth_cli)

experiment_name = "Classifier_demo"
exp = Experiment(workspace=ws, name=experiment_name)
print(exp.name, exp.workspace, sep="\t")

run_config_user_managed = RunConfiguration()
run_config_user_managed.environment.python.user_managed_dependencies = True


print("Submitting an experiment.")
src = ScriptRunConfig(
    source_directory="./code",
    script="training/train.py",
    run_config=run_config_user_managed,
)

run = exp.submit(src)

run.wait_for_completion(show_output=True, wait_post_processing=True)

if run.get_status() == "Failed":
    raise Exception(
        "Training on local failed with following run status: {} and logs: \n {}".format(
            run.get_status(), run.get_details_with_logs()
        )
    )

run_id = {}
run_id["run_id"] = run.id
run_id["experiment_name"] = run.experiment.name
with open("aml_config/run_id.json", "w") as outfile:
    json.dump(run_id, outfile)
