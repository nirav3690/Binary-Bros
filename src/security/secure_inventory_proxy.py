class SecureInventoryProxy:

    def __init__(self, real_inventory):
        self._real = real_inventory
        self._log  = []

    def is_available(self, item_id, user_role="user") -> bool:
        self._log.append(f"[Proxy] {user_role} checked availability of {item_id}")
        return self._real.is_available(item_id)

    def get_item(self, item_id, user_role="user"):
        self._log.append(f"[Proxy] {user_role} accessed item {item_id}")
        return self._real.get_item(item_id)

    def deduct_stock(self, item_id):
        self._log.append(f"[Proxy] stock deducted for {item_id}")
        return self._real.deduct_stock(item_id)

    def add_item(self, item):
        return self._real.add_item(item)

    def all_items(self):
        return self._real.all_items()

    def save(self):
        return self._real.save()

    def get_log(self):
        return list(self._log)