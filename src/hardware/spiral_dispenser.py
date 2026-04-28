from src.hardware.i_dispenser import IDispenser

class SpiralDispenser(IDispenser):
    def dispense(self, product_id): print(f"  [SpiralDispenser] Dispensing {product_id}"); return True
    def is_ready(self): return True
    def recalibrate(self): print("  [SpiralDispenser] Recalibrating...")
    def get_type(self): return "Spiral Dispenser"   