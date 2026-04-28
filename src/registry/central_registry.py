import json, os

class CentralRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        path = "data/config.json"
        if os.path.exists(path):
            with open(path) as f:
                self._config = json.load(f)
        else:
            self._config = {
                "kioskLocation": "Metro Station - Block A",
                "currency": "INR",
                "maxEmergencyQty": "2",
                "adminPassword": "admin123"
            }
            self._save()

    def _save(self):
        os.makedirs("data", exist_ok=True)
        with open("data/config.json", "w") as f:
            json.dump(self._config, f, indent=2)

    def get(self, key):
        return self._config.get(key, "N/A")

    def set(self, key, value):
        self._config[key] = value
        self._save()

    def all(self):
        return dict(self._config)