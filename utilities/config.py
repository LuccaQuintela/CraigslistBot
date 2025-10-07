import yaml
from pathlib import Path

class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, path=None):
        if not self._initialized:
            self._load(path)
            Config._initialized = True

    def _load(self, file_path):
        if file_path is None:
            file_path = Path(__file__).parent.parent / "config.yaml"
        try:
            with open(file_path, "r") as f:
                self.data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Project configuration file not found: {file_path}")

    def get_value(self, key, default=None):
        return self.data.get(key, default)

    @staticmethod
    def get(key, default=None):
        return Config().get_value(key, default)
