import yaml

CONFIG_PATH = "configs/dataset_config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)
    return config