from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import datetime
import pandas as pd
from fast_edit_distance import edit_distance
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(
    level=logging.INFO,
)

def getLatestModel():
    model_folder = '/app/data/models'
    model_files = os.listdir(model_folder)
    # print all the files in the models folder for debug
    logging.info(f"Model files: {model_files}")
    model_files.sort()
    latest_model = model_files[-1]
    model_date = latest_model.split('.')[0].split('_')[-1]
    fullpath = os.path.join(model_folder, latest_model)
    logging.info(f"Loading model {fullpath}")
    return fullpath, model_date

def indexRules(rules):
    models = {}
    for rule in rules:
        key = frozenset(rule[0])
        pred = list(rule[1])
        confidence = rule[2]

        length = len(key)
        if length not in models:
            models[length] = {}
        model = models[length]
        
        if key not in model:
            model[key] = []
            
        model[key].append({
            'recomendation': pred,
            'confidence': confidence
        })

    return models

def predict(model, playlist):
    rules = model['rules']
    recommendations = []
    for rule in rules:
        antecedent, consequent, confidence = rule
        if set(antecedent).issubset(playlist):
            for song in consequent:
                recommendations.append({
                    'name': song,
                    'confidence': confidence
                })
    # Remove duplicates while keeping the highest confidence
    unique_recommendations = {}
    for rec in recommendations:
        song = rec['name']
        if song not in unique_recommendations or rec['confidence'] > unique_recommendations[song]['confidence']:
            unique_recommendations[song] = rec
    return list(unique_recommendations.values())
            
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# model = pickle.load(open(latest_model, 'rb'))

class ModelFileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        if event.src_path.endswith('.pkl'):
            logging.info(f"New model detected: {event.src_path}")
            self.update_model()

    def update_model(self):
        latest_model, model_date = getLatestModel()
        self.app.model = pickle.load(open(latest_model, 'rb'))
        self.app.model_date = model_date
        logging.info(f"[INFO] Updated model to {latest_model}")

def start_model_monitor(app):
    event_handler = ModelFileHandler(app)
    observer = Observer()
    observer.schedule(event_handler, path='/app/data/models', recursive=False)
    observer.start()
    logging.info("[INFO] Started model monitor")
    return observer

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/data', methods=['POST'])
def handle_data():
    data = request.json
    # Process the data as needed
    return jsonify({"message": "Data received", "data": data}), 200

@app.route('/api/songs', methods=['POST'])
def get_songs():
    if not hasattr(app, 'model'):
        fullpath, model_date = getLatestModel()
        app.model = pickle.load(open(fullpath, 'rb'))
        app.model_date = model_date
    
    return jsonify({"songs": list(app.model['used_songs'])}), 200

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    
    playlist = data['songs'] 
    pred = predict(app.model, playlist)    
    
    # Process the data as needed
    return jsonify({
        "message": "Recommendation generated", 
        "songs": pred,
        "model_date": app.model_date
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 30746))
    observer = start_model_monitor(app)
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    finally:
        observer.stop()
        observer.join()