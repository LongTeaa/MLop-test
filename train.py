import pandas as pd
import numpy as np
import yaml
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model():
    # Load parameters
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    
    seed = params["base"]["random_seed"]
    test_size = params["data"]["test_size"]
    n_estimators = params["train"]["n_estimators"]
    max_depth = params["train"]["max_depth"]
    model_path = params["model"]["path"]
    
    np.random.seed(seed)
    
    # Generate dummy data
    X = np.random.rand(1000, 10)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )
    
    clf = RandomForestClassifier(
        n_estimators=n_estimators, 
        max_depth=max_depth, 
        random_state=seed
    )
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()