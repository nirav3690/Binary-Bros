from src.hardware.i_hardware_module import IHardwareModule

class RefrigerationModule(IHardwareModule):
    def __init__(self): self._attached = False
    def attach(self):   self._attached = True;  print("  [RefrigerationModule] Attached")
    def detach(self):   self._attached = False; print("  [RefrigerationModule] Detached")
    def get_status(self): return "active" if self._attached else "inactive"
    def get_name(self): return "Refrigeration Module"
    def is_attached(self): return self._attached