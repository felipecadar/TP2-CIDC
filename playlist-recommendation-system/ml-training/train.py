import pandas as pd
from fpgrowth_py import fpgrowth
import argparse
import pickle


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dataset", type=str, required=True)
    parser.add_argument("--output", type=str, default="./models")
    parser.add_argument("--min-support", type=float, default=0.05)
    parser.add_argument("--min-confidence", type=float, default=0.5)
    parser.add_argument("--run-grid-search", action="store_true")
    return parser.parse_args()

def generate_rules(data, min_support=0.05, min_confidence=0.1):
    itemSetList = data["tracks"].tolist()
    res = fpgrowth(itemSetList, minSupRatio=min_support, minConf=min_confidence)
    if not res:
        return None
    rules = res[1]
    return rules

def grid_search(args):
    min_supports = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15]
    min_confidences = [0.5]
    results = []
    for min_support in min_supports:
        for min_confidence in min_confidences:
            rules = generate_rules(data, min_support, min_confidence)
            rule_counts = {}
            if rules:
                for rule in rules:
                    rule_counts[len(rule[0])] = rule_counts.get(len(rule[0]), 0) + 1
            results.append(
                {
                    "min_support": min_support,
                    "min_confidence": min_confidence,
                    "rule_counts": rule_counts,
                    "rules": rules,
                }
            )
    return results

def recommend_songs(user_history, rules):
    recommendations = []
    for rule in rules:
        antecedent, consequent, confidence = rule
        if set(antecedent).issubset(user_history):
            recommendations.extend(consequent)
    recommendations = list(set(recommendations))  # Remove duplicates
    return recommendations

if __name__ == "__main__":

    args = parse()

    data = pd.read_csv(args.input_dataset)
    # track_uri,album_name,album_uri,artist_name,artist_uri,duration_ms,pid,track_name

    data = data.groupby("pid")["track_name"].apply(list).reset_index(name="tracks")

    itemSetList = data["tracks"].tolist()

    if args.run_grid_search:
        results = grid_search(args)
        for result in results:
            print(
                f"Min support: {result['min_support']}, Min confidence: {result['min_confidence']}, Rule counts: {result['rule_counts']}"
            )

        # save the results
        with open(f"{args.output}/grid_search_results.pkl", "wb") as f:
            pickle.dump(results, f)
        exit()

    # Generate rules
    rules = generate_rules(data, args.min_support, args.min_confidence)

    # count rules of all lengths
    rule_counts = {}
    for rule in rules:
        rule_counts[len(rule[0])] = rule_counts.get(len(rule[0]), 0) + 1

    print(rule_counts)

    used_songs = set()
    for rule in rules:
        for song in rule[0]:
            used_songs.add(song)

    # Save the trained model
    date = pd.to_datetime("today").strftime("%Y-%m-%d-%H-%M-%S")
    with open(f"{args.output}/model_{date}.pkl", "wb") as f:
        pickle.dump(
            {
                "rules": rules,
                "rule_counts": rule_counts,
                "used_songs": used_songs,
            },
            f,
        )
