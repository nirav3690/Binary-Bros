class KioskInterface:

    def __init__(self, kiosk):
        self._kiosk = kiosk

    def purchase_item(self, product_id, user_id) -> bool:
        return self._kiosk.purchase_item(product_id, user_id)

    def get_type(self) -> str:
        return self._kiosk.get_type()