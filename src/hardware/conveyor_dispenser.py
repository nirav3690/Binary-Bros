from src.hardware.i_dispenser import IDispenser

class ConveyorDispenser(IDispenser):
    def dispense(self, product_id): print(f"  [ConveyorDispenser] Moving {product_id}"); return True
    def is_ready(self): return True
    def recalibrate(self): print("  [ConveyorDispenser] Recalibrating belt...")
    def get_type(self): return "Conveyor Dispenser"