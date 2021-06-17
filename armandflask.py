from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.applications.xception import (
Xception, preprocess_input, decode_predictions)
import numpy as np
import os

app = Flask(__name__)

# dic = {0 : 'Cat', 1 : 'Dog'}

model = Xception(
    include_top=True,
    weights='imagenet')

# # model.make_predict_function()

# def predict(image_path):
#     # """Use Xception to label image"""
#     image_size = (299,299)
#     img = image.load_img(image_path, target_size=image_size)
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     predictions = model.predict(x)
#     results = decode_predictions(predictions, top=3)[0]
#     return jsonify(results)


# routes
@app.route("/", methods=['GET'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "YEAHHHHHHHHH!!!!!!! "

@app.route("/submit", methods = ['GET'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		image_path = "data/" + img.filename	
        
		

		p = predict(image_path)

	return render_template("index.html", prediction = p, image_path = image_path)

# Jeffs Help
@app.route("/predict/<image_path>")
def predict(image_path):
    # """Use Xception to label image"""

    image_path = os.path.join("..", "project3", "data", "1.jpg")

    image_size = (299,299)
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    results = decode_predictions(predictions, top=3)[0]

    return jsonify(results)


    

    



if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)