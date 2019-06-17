import json
import numpy as np
import os
import pickle
from sklearn.externals import joblib

from azureml.core.model import Model

def init():
  global model
  model_path = Model.get_model_path('cat_dog_classifier.pkl')
  model = joblib.load(model_path)
  
def run(raw_data):
  data = np.array(json.loads(raw_data)['data'])
  y_hat = model.predict(data)
  #return json.dumps(y_hat.tolist())
  return y_hat.tolist()