import numpy as np 
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('pickle_ml.pickle', 'rb'))