from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import logging
import time

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

def start_model_monitor(app, interval=10):
    def monitor():
        while True:
            try:
                latest_model, model_date = getLatestModel()
                if not hasattr(app, 'model_date') or app.model_date != model_date:
                    app.model = pickle.load(open(latest_model, 'rb'))
                    app.model_date = model_date
                    logging.info(f"[INFO] Updated model to {latest_model}")
            except Exception as e:
                logging.error(f"[ERROR] Failed to update model: {e}")
            time.sleep(interval)

    from threading import Thread
    monitor_thread = Thread(target=monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    logging.info("[INFO] Started model monitor")
    return monitor_thread

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
    monitor_thread = start_model_monitor(app)
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    finally:
        monitor_thread.join()