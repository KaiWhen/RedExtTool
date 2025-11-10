import json
import os
import sys


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
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


def load_all_path_data():
    path_data = {}
    if not os.path.exists('path_data/'):
        os.mkdir('path_data')
    i = 1
    for root, dirs, _ in os.walk('path_data/'):
        for dir in dirs:
            for _, _, files in os.walk(os.path.join(root, dir)):
                for file in files:
                    if file.endswith('.json'):
                        path_data[i] = load_json(os.path.join(root, dir, file))
                        i += 1
    return path_data
