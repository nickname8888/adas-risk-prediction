import json
import os


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def save_metadata(path, metadata):
    with open(path, "w") as f:
        json.dump(metadata, f, indent=4)