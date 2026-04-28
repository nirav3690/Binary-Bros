from src.hardware.i_hardware_module import IHardwareModule

# PATTERN: Decorator - concrete module
class SolarMonitorModule(IHardwareModule):
    def __init__(self): self._attached = False
    def attach(self):   self._attached = True;  print("  [SolarMonitor] Attached")
    def detach(self):   self._attached = False; print("  [SolarMonitor] Detached")
    def get_status(self): return "monitoring" if self._attached else "inactive"
    def get_name(self): return "Solar Monitor Module"
    def is_attached(self): return self._attached