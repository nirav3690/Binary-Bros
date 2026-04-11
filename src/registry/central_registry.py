
class CentralRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {
                "kioskLocation": "Metro Station - Block A",
                "currency":      "INR",
            }
        return cls._instance

    def get(self, key):
        return self._config.get(key, "N/A")

    def set(self, key, value):
        self._config[key] = value