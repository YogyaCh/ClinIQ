# config/settings.py

import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

TESSERACT_PATH = config.get("tesseract_path")
LLM_MODEL = config.get("llm_model", "llama3")
CHROMA_DB_DIR = config.get("chroma_db_dir")
REFERENCE_KNOWLEDGE_DIR = config.get("reference_knowledge_dir")
