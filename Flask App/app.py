from flask import Flask, render_template, redirect, request
# from xgboost import xception
import xgboost as xgb
import tensorflow
from tensorflow.keras.applications.xception import decode_predictions
import pandas as pd
import numpy as np
import pickle

# flask instance
app = Flask(__name__)
model = pickle.load(open('pickle_ml.pickle','rb'))

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict(image_path):
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    return  decode_predictions(predictions, top=3)[0]

# pred = decode_predictions(predictions, top=3)[0]
directory = "/Users/monicabustillos/Documents/project3/data"
prediction_list = []
for file in os.listdir(directory):
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

print(prediction_list)