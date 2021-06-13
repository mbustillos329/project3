from flask import Flask, render_template, redirect, request
from xgboost import xception
from tensorflow.keras.applications.xception import decode_predictions
import pandas as pd
import numpy as np
import pickle

# Create an instance of Flask
app = Flask(__name__)

model = pickle.load(open('best_xgb_model.pickle', 'rb'))


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    return render_template('index.html')


#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    #For rendering results on HTML GUI
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    output = ("Probability", "Prediction", "image")
    return  decode_predictions(predictions, top=3)[0]
    return render_template('index.html', prediction_text='This is a :{}'.format(output))


 

if __name__ == "__main__":
    app.run()