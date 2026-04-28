from src.kiosks.food_kiosk import FoodKiosk
from src.kiosks.pharmacy_kiosk import PharmacyKiosk
from src.kiosks.emergency_relief_kiosk import EmergencyReliefKiosk

class KioskFactory:

    @staticmethod
    def create(kiosk_type, dispenser, inventory, payment):
        if kiosk_type == "food":
            return FoodKiosk(dispenser, inventory, payment)
        elif kiosk_type == "pharmacy":
            return PharmacyKiosk(dispenser, inventory, payment)
        elif kiosk_type == "emergency":
            return EmergencyReliefKiosk(dispenser, inventory, payment)
        else:
            raise ValueError(f"Unknown kiosk type: {kiosk_type}")