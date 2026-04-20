from flask import Flask, request, jsonify
import pickle
import numpy as np
import yaml
import os

app = Flask(__name__)

# Load params to find model path
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)
model_path = params["model"]["path"]

model = None
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)