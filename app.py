from flask import Flask, request, jsonify, render_template
import redis
import time
import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

MODEL_FILENAME = 'iris_model.pkl'

# Attempt to load the model when the app starts
if os.path.exists(MODEL_FILENAME):
    model = joblib.load(MODEL_FILENAME)
    print("Loaded existing model from disk.")
else:
    model = None
    print("No model found. Needs training.")

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def home():
    count = get_hit_count()
    return render_template('index.html', count=count)

@app.route('/train', methods=['GET'])
def train_model():
    global model
    
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the trained model to the hard drive!
    joblib.dump(model, MODEL_FILENAME)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    return jsonify({
        "status": "success",
        "message": "Model trained and saved to disk successfully!",
        "accuracy": f"{accuracy * 100:.2f}%",
        "classes": list(iris.target_names)
    })

@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        return jsonify({"error": "Model not trained. Visit /train first."}), 400
    
    data = request.get_json()
    if not data or 'features' not in data:
        return jsonify({"error": "Please provide 'features' array in JSON body."}), 400
    
    try:
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        
        iris = load_iris()
        predicted_class = iris.target_names[prediction[0]]
        
        return jsonify({
            "status": "success",
            "prediction_id": int(prediction[0]),
            "predicted_class": predicted_class
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400