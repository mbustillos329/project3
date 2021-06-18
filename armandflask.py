from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.applications.xception import (
Xception, preprocess_input, decode_predictions)
import numpy as np
import os
import json
import pandas as pd

app = Flask(__name__)

model = Xception(
    include_top=True,
    weights='imagenet')

# Jeffs Help

@app.route("/predict")
def predict():
    # """Use Xception to label image"""
    image_path = request.args.get("filename")
    print(image_path)
    image_size = (299,299)
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    results = decode_predictions(predictions, top=3)[0]
    df = pd.DataFrame(results, columns=["id", "prediction", "probability"])
    new_dict = df.to_dict(orient="records")
 
    return jsonify(new_dict)