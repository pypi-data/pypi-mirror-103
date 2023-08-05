import os
import sys
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.append(CURRENT_DIR)


def _load_impacts():
    files = list(filter(lambda f: f.endswith('.jsonld'), os.listdir(CURRENT_DIR)))
    impacts = []
    for filename in files:
        with open(os.path.join(CURRENT_DIR, filename), 'r') as file:
            impacts.append(json.load(file))
    return impacts
