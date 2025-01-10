from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd
import pickle
import os
from fpgrowth_py import fpgrowth
from datetime import datetime
from threading import Thread

app = Flask(__name__)
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/data/uploads')
MODELS_FOLDER = os.environ.get('MODELS_FOLDER', '/app/data/models')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODELS_FOLDER'] = MODELS_FOLDER
training_status = "Idle"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
if not os.path.exists(MODELS_FOLDER):
    os.makedirs(MODELS_FOLDER)

def getLatestModel(model_folder='/app/data/models'):
    model_files = os.listdir(model_folder)
    # print all the files in the models folder for debug
    model_files.sort()
    latest_model = model_files[-1]
    model_date = latest_model.split('.')[0].split('_')[-1]
    fullpath = os.path.join(model_folder, latest_model)
    return fullpath, model_date

def generate_rules(data, min_support=0.05, min_confidence=0.1):
    itemSetList = data["tracks"].tolist()
    res = fpgrowth(itemSetList, minSupRatio=min_support, minConf=min_confidence)
    if not res:
        return None
    rules = res[1]
    return rules

def get_trained_models():
    model_files = [f for f in os.listdir(app.config['MODELS_FOLDER']) if f.startswith('model_') and f.endswith('.pkl')]
    model_files.sort(reverse=True)  # Sort in descending order
    trained_models = []
    for model_file in model_files:
        model_date = model_file.split('.')[0].split('_')[-1]
        trained_models.append({
            'filename': model_file,
            'date': model_date,
            'is_latest': model_file == model_files[0]  # The first file is the most recent
        })
    return trained_models

@app.route('/')
def index():
    trained_models = get_trained_models()
    return render_template('index.html', trained_models=trained_models, training_status=training_status)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)
        data = data.groupby("pid")["track_name"].apply(list).reset_index(name="tracks")
        thread = Thread(target=train_model, args=(data,))
        thread.start()
        return redirect(url_for('index'))

@app.route('/training-status')
def training_status_endpoint():
    return jsonify(status=training_status)

def train_model(data):
    global training_status
    training_status = "Training in progress"
    try:
        rules = generate_rules(data, min_support=0.05, min_confidence=0.5)
        rule_counts = {}
        for rule in rules:
            rule_counts[len(rule[0])] = rule_counts.get(len(rule[0]), 0) + 1
        used_songs = set()
        for rule in rules:
            for song in rule[0]:
                used_songs.add(song)
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        model_filename = f'/app/data/models/model_{timestamp}.pkl'
        with open(model_filename, 'wb') as f:
            pickle.dump({
                "rules": rules,
                "rule_counts": rule_counts,
                "used_songs": used_songs,
            }, f)
        training_status = "Training completed successfully"
    except Exception as e:
        training_status = f"Training failed: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 52020))
    app.run(debug=True, host='0.0.0.0', port=port)