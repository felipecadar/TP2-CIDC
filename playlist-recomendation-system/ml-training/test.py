import pickle
import pandas as pd
import argparse
import os
from fast_edit_distance import edit_distance

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model")
    parser.add_argument("--songs")
    return parser.parse_args()

def getLatestModel(model_folder):
    model_files = os.listdir(model_folder)
    model_files.sort()
    latest_model = model_files[-1]
    fullpath = os.path.join(model_folder, latest_model)
    print(f"Loading model {fullpath}")
    return fullpath

def normalizeName(name):
    # Turn Down for What - Official Remix -> Turn Down for What
    # Turn Down for What - Official Remix (feat. Lil Jon) -> Turn Down for What
    # Turn Down for What REMIX -> Turn Down for What
    # Turn Down for What - Remix -> Turn Down for What
    # Turn Down for What - Remix - Explicit -> Turn Down for What
    # Turn Down for What (remix) -> Turn Down for What
    
    # remove everything after '-'
    name = name.split(' -')[0].strip()
    # remove everything after '('
    name = name.split('(')[0].strip()
    # remove everything after 'REMIX'
    name = name.split('REMIX')[0].strip()
    # remove everything after 'Remix'
    name = name.split('Remix')[0].strip()
    # remove everything after 'remix'
    name = name.split('remix')[0].strip()
    
    return name

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

def predict(model, songs):
    rules = model['rules']
    used_songs = model['used_songs']
    
    # for each song, get the closest string in the used_songs
    close_songs = [getClosestString(used_songs, song) for song in songs]
    for s1, s2 in zip(songs, close_songs):
        if s1 != s2:
            print(f"{s1} -> {s2}")
    
    length = len(songs)
    model = rules.get(length, {})
    return model.get(frozenset(close_songs), [])

def getClosestString(songs, song):
    min_distance = float('inf')
    min_perc = 0.1 # edit distance should be at most 20% of the string length
    closest = song
    for s in songs:
        min_length =len(song)
        distance = edit_distance(song[:min_length], s[:min_length])
        if distance < min_distance and distance < min_perc * min_length:
            min_distance = distance
            closest = s
    return closest

if __name__ == "__main__":
    args = parse()
    model = pickle.load(open(getLatestModel(args.model), 'rb'))
    model['rules'] = indexRules(model['rules'])
    
    songs = pd.read_csv(args.songs)['track_name'].tolist()
    # songs = [normalizeName(song) for song in songs]
    
    for song in songs:
        recommendations = predict(model, [song])
        if len(recommendations) > 0:
            print(f"Recommendations for {song}:")
            for rec in recommendations:
                print(f"  - {rec['recomendation']} with confidence {rec['confidence']}")
            print()
            
    # print(model.keys())