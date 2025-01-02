from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import datetime
import pandas as pd

# models path 
models = '/app/models'
# model is "model_Y-m-d-H-M-S.pkl"
# get the latest model
model_files = os.listdir(models)
model_files.sort()
latest_model = model_files[-1]
model_date = latest_model.split('.')[0].split('_')[-1]

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
app.model = pickle.load(open('/app/models/' + latest_model, 'rb'))
print(f"[INFO] Loaded model {latest_model}")

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/data', methods=['POST'])
def handle_data():
    data = request.json
    # Process the data as needed
    return jsonify({"message": "Data received", "data": data}), 200

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    # Process the data as needed
    return jsonify({
        "message": "Recommendation generated", 
        "data": data,
        "songs": ["Bottle It Up - Acoustic Mixtape", "No Faith in Brooklyn (feat. Jhameel)"]
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 30502))
    app.run(host='0.0.0.0', port=port)