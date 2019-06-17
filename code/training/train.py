import pickle
import os, json
import numpy as np
import subprocess
from sklearn.externals import joblib
from typing import Tuple, List
from azureml.core import Workspace
from azureml.core.run import Run
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
args = parser.parse_args()

data_folder = os.path.join(args.data_folder, 'dataset')
print('Data folder:', data_folder)

train_path = os.path.join(data_folder, 'train_set')
test_path = os.path.join(data_folder, 'test_set')

#initializing cnn
classifier = Sequential()

#1st layer: Convolutional layer
classifier.add(Convolution2D(32,3,3,input_shape=(64,64,3), activation = 'relu'))

#2nd layer: pooling layer
classifier.add(MaxPooling2D(pool_size=(2,2)))

#3rd layer: flattening
classifier.add(Flatten())

#4th layer: full connection
classifier.add(Dense(output_dim = 128, activation='relu'))
classifier.add(Dense(output_dim = 1, activation='sigmoid'))

#compiliation
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#fitting images into cnn
from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set1 = train_datagen.flow_from_directory(
        train_path,
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

testing_set = test_datagen.flow_from_directory(
        test_path,
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

classifier.fit_generator(
        training_set1,
        steps_per_epoch=8000,
        epochs=25,
        validation_data=testing_set,
        validation_steps=2000)

model_name = "cat_dog_classifier.pkl"

run = Run.get_submitted_run()

with open(model_name, "wb") as file:
    joblib.dump(value=classifier, filename=model_name)

run.upload_file(name="./outputs/" + model_name, path_or_stream=model_name)
print("Uploaded the model {} to experiment {}".format(model_name, run.experiment.name))
dirpath = os.getcwd()
print(dirpath)

print("Following files are uploaded ")
print(run.get_file_names())
run.complete()