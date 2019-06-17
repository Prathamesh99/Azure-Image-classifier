import azureml.core
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import Run
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.runconfig import RunConfiguration
import os, json, sys

auth_cli = AzureCliAuthentication()

ws = Workspace.using_config(path="aml_config/config.json", auth=auth_cli)

try:
    with open("aml_config/run_id.json") as f:
        config = json.load(f)
    if not config["run_id"]:
        raise Exception("No new model to register as production model perform better")
except:
    print("No new model to register as production model perform better")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

run_id = config["run_id"]
experiment_name = config["experiment_name"]
exp = Experiment(workspace=ws, name=experiment_name)

run = Run(experiment=exp, run_id=run_id)
names = run.get_file_names
names()
print("Run ID for last run: {}".format(run_id))
model_local_dir = "model"
os.makedirs(model_local_dir, exist_ok=True)

model_name = "cat_dog_classifier.pkl"
run.download_file(
    name="./outputs/" + model_name, output_file_path="./model/" + model_name
)
print("Downloaded model {} to Project root directory".format(model_name))
os.chdir("./model")

model = Model.register(
    model_path=model_name,  # this points to a local file
    model_name=model_name,  # this is the name the model is registered as
    tags={"area": "cat dog", "type": "image classifier", "run_id": run_id},
    description="Image classification model",
    workspace=ws,
)
os.chdir("..")
print(
    "Model registered: {} \nModel Description: {} \nModel Version: {}".format(
        model.name, model.description, model.version
    )
)

model_json = {}
model_json["model_name"] = model.name
model_json["model_version"] = model.version
model_json["run_id"] = run_id
with open("aml_config/model.json", "w") as outfile:
    json.dump(model_json, outfile)
