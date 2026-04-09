import json
import os
from pathlib import Path


def load_env_file(env_path=None):
    if env_path is None:
        env_path = Path(__file__).resolve().parent / ".env"
    else:
        env_path = Path(env_path).expanduser().resolve()

    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if ((value.startswith('"') and value.endswith('"')) or
                (value.startswith("'") and value.endswith("'"))):
            value = value[1:-1]

        if key and key not in os.environ:
            os.environ[key] = value


def load_config():
    load_env_file()
    config_path = Path(__file__).resolve().parent / "appsettings.json"
    with config_path.open('r', encoding="utf-8") as f:
        config_data = json.load(f)
    return config_data
