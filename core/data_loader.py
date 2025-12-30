import json
import os
import sys


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_temp_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def load_json(filename):
    try:
        filepath = get_resource_path(filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return {}


def load_forest_path_data():
    path_data = {}
    if not os.path.exists('path_data/forest/'):
        os.mkdir('path_data/forest/')
    i = 1
    for root, dirs, _ in os.walk('path_data/forest/'):
        for dir in dirs:
            for _, _, files in os.walk(os.path.join(root, dir)):
                for file in files:
                    if file.endswith('.json'):
                        path_data[i] = load_json(os.path.join(root, dir, file))
                        i += 1
    return path_data

def load_surge_path_data():
    path_data = {}
    if not os.path.exists('path_data/surge/'):
        os.mkdir('path_data/surge/')
    for root, dirs, _ in os.walk('path_data/surge/'):
        for _, _, files in os.walk(os.path.join(root)):
            for file in files:
                if file.endswith('surge.json'):
                    path_data["surge"] = load_json(os.path.join(root, file))
    return path_data
