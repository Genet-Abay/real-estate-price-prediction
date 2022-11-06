import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import pickle
import traceback
import os

app = Flask(__name__)
@app.route('/')
def welcome():
    return "Welcome to the real estate price prediction application!"

@app.route('/predict', methods=['POST'])
def predict():
    if model:
        try:
            json_ = request.json
            print(json_)
            df = pd.DataFrame(json_)
            prediction = list(model.predict(df))
            return jsonify({'prediction': prediction[0]})

        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')


if __name__ == '__main__':
    with open('model.pkl', 'rb') as pickle_file:
        model = pickle.load(pickle_file) # Load "model.pkl"
    print ('Model loaded')
    app.run(debug=True, host='0.0.0.0', port=os.environ.get("PORT",  80))