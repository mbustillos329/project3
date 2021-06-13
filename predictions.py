# dependencies
import matplotlib.pyplot as plt
import os
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)

# xception model
model = Xception(
    include_top=True,
    weights='imagenet')

# default image size
image_size = (299,299)

# load image and resize 
image_path = os.path.join("..", "project3", "data")
print(image_path)
img = image.load_img(image_path, target_size=image_size)
plt.imshow(img)

# preprocess image
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# predictions
predictions = model.predict(x)
print('Predicted:', decode_predictions(predictions, top=3)[0])
plt.imshow(img)

# Refactor above steps into reusable function
def predict(image_path):
    """Use Xception to label image"""
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    return  decode_predictions(predictions, top=3)[0]

image_path = os.path.join("..", "project3", "data")

cur_preds = predict(image_path)
cur_preds

# pred = decode_predictions(predictions, top=3)[0]
directory = "/project3/data"
prediction_list = []
for file in os.listdir(directory)[:3]:
    if file.endswith(".jpg"):
        image_path = os.path.join("..", "project3", "data", file)
        variable = predict(image_path)
#         print(variable)
        for item in variable:
            prediction_list.append({
                'Image': file,
                'Prediction': item[1],
                'Probability': item[2],
            })


prediction_list 