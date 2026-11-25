from pathlib import Path
from typing import Any
import yaml

def load_config(path: str | Path = "config.yaml") -> dict[str, Any]:
    """Читает конфиг файл и возращает словарь"""
    config_path = Path(path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path.resolve()}")
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    if not isinstance(config, dict):
        raise ValueError(f"Ожидался словарь в конфиге, получено: {type(config).__name__}")
    return config