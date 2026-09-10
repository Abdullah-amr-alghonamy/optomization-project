from pathlib import Path
import json


DRAFTS_DIR = Path(__file__).resolve().parent.parent / "drafts"

DRAFTS_DIR.mkdir(exist_ok=True)

# saving draft
def save_draft(name, data):
    file_path = DRAFTS_DIR / f"{name}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path

# loading draft
def load_draft(name):
    file_path = DRAFTS_DIR / f"{name}.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def list_drafts():
    return sorted(
        file.stem
        for file in DRAFTS_DIR.glob("*.json")
    )