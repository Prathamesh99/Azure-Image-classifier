import azureml.core
from azureml.core.image import Image, ContainerImage
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
import os, json, sys
from azureml.core.model import Model
auth_cli = AzureCliAuthentication()

ws = Workspace.using_config(path="aml_config/config.json", auth=auth_cli)

try:
    with open("aml_config/model.json") as f:
        config = json.load(f)
except:
    print("No new model to register thus no need to create new scoring image")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

model_name = config["model_name"]
model_version = config["model_version"]

model_list = Model.list(workspace=ws)
model, = (m for m in model_list if m.version == model_version and m.name == model_name)
print(
    "Model picked: {} \nModel Description: {} \nModel Version: {}".format(
        model.name, model.description, model.version
    )
)

os.chdir("./code/scoring")
image_name = "image_classifier_score"

image_config = ContainerImage.image_configuration(
    execution_script="score.py",
    runtime="python-slim",
    conda_file="conda_dependencies.yml",
    description="Image with cat dog classifier model",
    tags={"area": "cat dog", "type": "image classifier"},
)

image = Image.create(
    name=image_name, models=[model], image_config=image_config, workspace=ws
)

image.wait_for_creation(show_output=True)
os.chdir("../..")

if image.creation_state != "Succeeded":
    raise Exception("Image creation status: {image.creation_state}")

print(
    "{}(v.{} [{}]) stored at {} with build log {}".format(
        image.name,
        image.version,
        image.creation_state,
        image.image_location,
        image.image_build_log_uri,
    )
)

# Writing the image details to /aml_config/image.json
image_json = {}
image_json["image_name"] = image.name
image_json["image_version"] = image.version
image_json["image_location"] = image.image_location
with open("aml_config/image.json", "w") as outfile:
    json.dump(image_json, outfile)

