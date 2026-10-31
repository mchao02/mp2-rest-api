import json
import logging
from pathlib import Path

import pandas as pd
import yaml

logger = logging.getLogger(__name__)

def load_csv(filepath):
    """Load a CSV file into a DataFrame"""
    data = pd.read_csv(filepath)
    logger.info(f"Load CSV file: {filepath} ({len(data)} rows)")
    return data

def load_json(filepath):
    """Load a JSON file"""
    with open(filepath, encoding="utf=8") as file:
        data = json.load(file)
    logger.info(f"Loaded JSON file: {filepath}")
    return data
def load_yaml(filepath):
    """Load a YAML file"""
    with open(filepath, encoding="utf=8") as file:
        data = yaml.safe_load(file)

    logger.info(f"loaded YAML file: {filepath}")
    return data
def load_data(filepath):
    """Load a file based on its extensions"""
    path = Path(filepath)
    extension = path.suffix.lower()

    if extension == ".csv":
        return load_csv(path)
    elif extension == ".json":
        return load_json(path)
    elif extension == ".yaml":
        return load_yaml(path)

    logger.error(f"Unsupporte file format: {extension}")
    raise ValueError(f"Unsupported file format: {extension}")