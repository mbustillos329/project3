from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.applications.xception import (
Xception, preprocess_input, decode_predictions)
import numpy as np
import os
import json
import pandas as pd
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from flask import Flask

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


model = Xception(
    include_top=True,
    weights='imagenet')

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()


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


if __name__ == "__main__":
    app.run()
