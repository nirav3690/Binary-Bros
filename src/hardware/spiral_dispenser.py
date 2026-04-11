from src.hardware.i_dispenser import IDispenser

class SpiralDispenser(IDispenser):

    def dispense(self, product_id: str) -> bool:
        print(f"  [SpiralDispenser] Dispensing: {product_id}")
        return True

    def is_ready(self) -> bool:
        return True