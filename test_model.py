import pytest
import pickle
import os
import yaml
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def load_params():
    with open("params.yaml", "r") as f:
        return yaml.safe_load(f)

def test_model_exists():
    params = load_params()
    model_path = params["model"]["path"]
    assert os.path.exists(model_path), f"Model file {model_path} not found"

def test_model_accuracy():
    params = load_params()
    model_path = params["model"]["path"]
    accuracy_threshold = params["model"]["accuracy_threshold"]
    
    # Load model
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
    
    # Generate test data using same seed as training to verify logic
    seed = params["base"]["random_seed"]
    test_size = params["data"]["test_size"]
    np.random.seed(seed)
    X = np.random.rand(1000, 10)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )
    
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    assert accuracy >= accuracy_threshold, f"Accuracy {accuracy} is below threshold {accuracy_threshold}"

def test_inference_data_format():
    params = load_params()
    model_path = params["model"]["path"]
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
        
    # Test valid input (10 features)
    valid_input = np.random.rand(1, 10)
    prediction = clf.predict(valid_input)
    assert len(prediction) == 1
    assert prediction[0] in [0, 1]

if __name__ == "__main__":
    pytest.main([__file__])