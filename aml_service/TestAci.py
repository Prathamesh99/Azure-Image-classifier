import numpy as np
import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.authentication import AzureCliAuthentication
from keras.preprocessing import image

auth_cli = AzureCliAuthentication()
ws = Workspace(path="aml_config/config.json", auth=auth_cli)

try:
    with open("aml_config/aci_webservice.json") as f:
        config = json.load(f)
except:
    print("No new model, thus no deployment on ACI")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

service_name = config["aci_name"]
# Get the hosted web service
service = Webservice(name=service_name, workspace=ws)

X_test = image.load_img('./dataset/single_prediction/cat_or_dog_2.jpg', target_size = (64,64))
X_test = np.expand_dims(X_test, axis=0)
X_test = X_test.reshape(1,64,64,3)

index = np.random.permutation(X_test.shape[0])[0:1]
test_samples = json.dumps({"data": X_test[index].tolist()})
test_samples = bytes(test_samples, encoding = 'utf8')

try:
    prediction = service.run(input_data=test_samples)
    print(prediction)
except Exception as e:
    result = str(e)
    print(result)
    raise Exception("ACI service is not working as expected")
