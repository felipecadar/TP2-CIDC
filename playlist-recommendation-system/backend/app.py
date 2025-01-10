from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import datetime
import pandas as pd
from fast_edit_distance import edit_distance
import logging

logging.basicConfig(
    level=logging.DEBUG,
)

def getLatestModel():
    model_folder = '/app/models'
    model_files = os.listdir(model_folder)
    # print all the files in the models folder for debug
    logging.debug(f"Model files: {model_files}")
    model_files.sort()
    latest_model = model_files[-1]
    model_date = latest_model.split('.')[0].split('_')[-1]
    fullpath = os.path.join(model_folder, latest_model)
    logging.debug(f"Loading model {fullpath}")
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
    used_songs = model['used_songs']

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
            
def getClosestString(songs_search_list, song):
    closest = song
    # logging.debug(f"Searching {song} in a list of {len(songs_search_list)} songs")
    # logging.debug('\n'.join(songs_search_list))
    for s in songs_search_list:
        if song in s and len(s) < len(closest):
            closest = s
            # logging.debug(f" found {song} -> {s}")
    return closest

latest_model, model_date = getLatestModel()
# songs_db = pd.read_csv('/app/dataset/2023_spotify_songs.csv')['track_name'].tolist()

#get version file
if not os.path.exists('/app/version.txt'):
    with open('/app/version.txt', 'w') as f:
        f.write('0.0.1\n')
        f.write(model_date)
        
# load version and last model date
with open('/app/version.txt', 'r') as f:
    version = f.readline().strip()
    last_model_date = f.readline().strip()
    
# check if we need to bump the version
if last_model_date != model_date:
    version = version.split('.')
    version[-1] = str(int(version[-1]) + 1)
    version = '.'.join(version)
    with open('/app/version.txt', 'w') as f:
        f.write(version + '\n')
        f.write(model_date)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
model = pickle.load(open(latest_model, 'rb'))
# model['rules'] = indexRules(model['rules'])

app.model = model
logging.debug(f"[INFO] Loaded model {latest_model}")

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
    return jsonify({"songs": list(model['used_songs'])}), 200

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    
    playlist = data['songs'] 
    pred = predict(app.model, playlist)    
    
    # Process the data as needed
    return jsonify({
        "message": "Recommendation generated", 
        "songs": pred,
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 52019))
    app.run(host='0.0.0.0', port=port, debug=True)