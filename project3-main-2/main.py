import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.xception import (
Xception, preprocess_input, decode_predictions)
import numpy as np
from keras.preprocessing import image
import pandas as pd
from flask import Flask, render_template, request, jsonify

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

model = Xception(
    include_top=True,
    weights='imagenet')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        file.save(file_path)
        image_size = (299,299)
        img = image.load_img(file_path, target_size=image_size)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        predictions = model.predict(x)
        results = decode_predictions(predictions, top=3)[0]
        df = pd.DataFrame(results, columns=["id", "prediction", "probability"])
        new_dict = df.to_dict(orient="records")
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify(new_dict)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()