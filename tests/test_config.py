from pathlib import Path
import pytest
from moexrisk.config import load_config

def test_load_valid_config(tmp_path: Path) -> None:
    """Проверяет чтение корректного YAML-файла (как по str, так и по Path)."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
        data:
          date_start: "2014-01-01"
          date_finish: null
          tickers:
            - SBER
            - GAZP
        risk:
          confidence_levels: [0.95, 0.99]
          horizons: [1, 5, 21]
        """,
        encoding="utf-8",
    )

    # Проверяем передачу пути как объекта Path и как строки str
    cfg_from_path = load_config(config_file)
    cfg_from_str = load_config(str(config_file))

    assert cfg_from_path == cfg_from_str
    assert cfg_from_path["data"]["tickers"] == ["SBER", "GAZP"]
    assert cfg_from_path["data"]["date_finish"] is None
    assert cfg_from_path["risk"]["horizons"] == [1, 5, 21]


def test_load_config_file_not_found(tmp_path: Path) -> None:
    """Проверяет выброс FileNotFoundError при отсутствии файла."""
    missing_file = tmp_path / "non_existent.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(missing_file)


def test_load_empty_or_invalid_structure_config(tmp_path: Path) -> None:
    """Проверяет выброс ValueError, если файл пустой или содержит список вместо словаря."""
    empty_file = tmp_path / "empty.yaml"
    empty_file.write_text("", encoding="utf-8")

    list_file = tmp_path / "list.yaml"
    list_file.write_text("- SBER\n- GAZP\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Ожидался словарь"):
        load_config(empty_file)

    with pytest.raises(ValueError, match="Ожидался словарь"):
        load_config(list_file)


def test_project_root_config_is_valid() -> None:
    """Интеграционный тест: проверяет, что реальный config.yaml в корне проекта валиден."""
    project_config = Path(__file__).resolve().parents[1] / "config.yaml"
    cfg = load_config(project_config)

    assert "data" in cfg
    assert "risk" in cfg
    assert len(cfg["data"]["tickers"]) >= 15
    assert cfg["risk"]["horizons"] == [1, 5, 21]