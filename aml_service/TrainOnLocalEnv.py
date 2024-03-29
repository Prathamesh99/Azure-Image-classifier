from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import ScriptRunConfig

from azureml.core.authentication import AzureCliAuthentication
auth_cli = AzureCliAuthentication()

ws = Workspace.from_config(path='aml_config/config.json')

experiment_name = "Classifier-demo"
exp = Experiment(workspace=ws, name=experiment_name)
print(exp.name, exp.workspace, sep="\t")

# Editing a run configuration property on-fly.
run_config_system_managed = RunConfiguration()
# Use a new conda environment that is to be created from the conda_dependencies.yml file
run_config_system_managed.environment.python.user_managed_dependencies = False
# Automatically create the conda environment before the run
run_config_system_managed.prepare_environment = True

print("Submitting an experiment to new conda virtual env")
src = ScriptRunConfig(
    source_directory="./code",
    script="training/train.py",
    run_config=run_config_user_managed,
)
run = exp.submit(src)

# Shows output of the run on stdout.
run.wait_for_completion(show_output=True, wait_post_processing=True)

# Raise exception if run fails
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
