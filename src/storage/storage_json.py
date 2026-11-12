
import json
from pathlib import Path

from logs import logger


def read_json(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.info("Successfully read JSON file: %s", file_path.name)
        return data

    except FileNotFoundError:
        logger.exception("JSON file not found: %s", file_path)
        raise

    except json.JSONDecodeError:
        logger.exception("Invalid JSON format: %s", file_path)
        raise

    except OSError:
        logger.exception("Error reading JSON file: %s", file_path)
        raise


def write_json(file_path: Path, data):
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logger.info("Successfully updated JSON file: %s", file_path.name)

    except (OSError, TypeError):
        logger.exception("Error writing JSON file: %s", file_path)
        raise
