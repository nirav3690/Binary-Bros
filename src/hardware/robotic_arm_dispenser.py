from src.hardware.i_dispenser import IDispenser

class RoboticArmDispenser(IDispenser):
    def dispense(self, product_id): print(f"  [RoboticArm] Picking {product_id}"); return True
    def is_ready(self): return True
    def recalibrate(self): print("  [RoboticArm] Recalibrating arm...")
    def get_type(self): return "Robotic Arm Dispenser"