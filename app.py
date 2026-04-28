from flask import Flask, request, jsonify, render_template
import json, os

from src.registry.central_registry import CentralRegistry
from src.hardware.spiral_dispenser import SpiralDispenser
from src.hardware.robotic_arm_dispenser import RoboticArmDispenser
from src.hardware.conveyor_dispenser import ConveyorDispenser
from src.hardware.refrigeration_module import RefrigerationModule
from src.hardware.solar_monitor_module import SolarMonitorModule
from src.inventory.product import Product
from src.inventory.product_bundle import ProductBundle
from src.inventory.inventory_manager import InventoryManager
from src.payment.credit_card_adapter import CreditCardAdapter
from src.payment.upi_adapter import UPIAdapter
from src.payment.digital_wallet_adapter import DigitalWalletAdapter
from src.payment.credit_card_gateway import CreditCardGateway
from src.commands.purchase_item_command import PurchaseItemCommand
from src.commands.refund_command import RefundCommand
from src.commands.restock_command import RestockCommand
from src.security.secure_inventory_proxy import SecureInventoryProxy
from src.kiosks.kiosk_factory import KioskFactory

app = Flask(__name__)

registry  = CentralRegistry()
inv_mgr   = InventoryManager()
inv_mgr.load()
proxy     = SecureInventoryProxy(inv_mgr)

dispensers = {
    "spiral":   SpiralDispenser(),
    "robotic":  RoboticArmDispenser(),
    "conveyor": ConveyorDispenser()
}
payments = {
    "credit": CreditCardAdapter(CreditCardGateway()),
    "upi":    UPIAdapter(),
    "wallet": DigitalWalletAdapter()
}
modules = {
    "refrigeration": RefrigerationModule(),
    "solar":         SolarMonitorModule()
}

active_kiosk_type    = "food"
active_dispenser_key = "spiral"
active_payment_key   = "credit"
active_kiosk         = None

def rebuild_kiosk():
    global active_kiosk
    dispenser = dispensers[active_dispenser_key]
    payment   = payments[active_payment_key]
    active_kiosk = KioskFactory.create(
        active_kiosk_type, dispenser, proxy, payment)

rebuild_kiosk()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "kioskType":    active_kiosk_type,
        "dispenser":    dispensers[active_dispenser_key].get_type(),
        "payment":      active_payment_key,
        "location":     registry.get("kioskLocation"),
        "currency":     registry.get("currency"),
        "modules":      {k: m.get_status() for k, m in modules.items()}
    })

@app.route("/api/products")
def get_products():
    items = []
    for item in proxy.all_items():
        items.append({
            "id":    item.get_id(),
            "name":  item.get_name(),
            "price": item.get_price(),
            "stock": item.get_available_stock(),
            "available": item.is_available()
        })
    return jsonify(items)

@app.route("/api/product-flags")
def product_flags():
    """Return kiosk-specific flags per product (e.g. prescription required)."""
    flags = {}
    if active_kiosk_type == "pharmacy":
        from src.kiosks.pharmacy_kiosk import PharmacyKiosk
        kiosk = active_kiosk
        for item in proxy.all_items():
            pid = item.get_id()
            flags[pid] = {
                "prescription_required": kiosk.requires_prescription(pid) if hasattr(kiosk, "requires_prescription") else False
            }
    return jsonify(flags)

@app.route("/api/purchase", methods=["POST"])
def purchase():
    data       = request.json
    product_id = data.get("product_id")
    user_id    = data.get("user_id", "guest")

    if active_kiosk_type == "emergency":
        max_qty = int(registry.get("maxEmergencyQty"))
        count   = _get_user_count(user_id)
        if count >= max_qty:
            return jsonify({"success": False,
                "message": f"Purchase limit of {max_qty} reached for emergency mode"}), 403

    cmd     = PurchaseItemCommand(product_id, user_id, proxy, payments[active_payment_key])
    success = cmd.execute()

    if success:
        dispensers[active_dispenser_key].dispense(product_id)
        if active_kiosk_type == "emergency":
            _increment_user_count(user_id)
        return jsonify({"success": True, "txn_id": cmd.get_txn_id(),
            "message": "Purchase successful"})
    else:
        return jsonify({"success": False,
            "message": "Purchase failed — product unavailable or payment error"}), 400

@app.route("/api/refund", methods=["POST"])
def refund():
    data   = request.json
    txn_id = data.get("txn_id")
    cmd    = RefundCommand(txn_id, payments[active_payment_key])
    result = cmd.execute()
    return jsonify({"success": result,
        "message": "Refund processed" if result else "Refund failed"})

@app.route("/api/restock", methods=["POST"])
def restock():
    data       = request.json
    product_id = data.get("product_id")
    quantity   = int(data.get("quantity", 0))
    cmd        = RestockCommand(product_id, quantity, inv_mgr)
    result     = cmd.execute()
    return jsonify({"success": result,
        "message": f"Restocked {quantity} units" if result else "Restock failed"})

@app.route("/api/transactions")
def transactions():
    path = "data/transactions.json"
    if not os.path.exists(path):
        return jsonify([])
    with open(path) as f:
        return jsonify(json.load(f))

@app.route("/api/switch-kiosk", methods=["POST"])
def switch_kiosk():
    global active_kiosk_type, active_dispenser_key, active_payment_key
    data = request.json
    active_kiosk_type    = data.get("kiosk_type", active_kiosk_type)
    active_dispenser_key = data.get("dispenser",  active_dispenser_key)
    active_payment_key   = data.get("payment",    active_payment_key)
    rebuild_kiosk()
    return jsonify({"success": True,
        "message": f"Switched to {active_kiosk_type} kiosk"})

@app.route("/api/module", methods=["POST"])
def toggle_module():
    data   = request.json
    mod    = data.get("module")
    action = data.get("action")
    if mod in modules:
        if action == "attach":
            modules[mod].attach()
        else:
            modules[mod].detach()
        return jsonify({"success": True, "status": modules[mod].get_status()})
    return jsonify({"success": False}), 400

@app.route("/api/config", methods=["GET"])
def get_config():
    cfg = registry.all()
    cfg.pop("adminPassword", None)
    return jsonify(cfg)

@app.route("/api/config", methods=["PUT"])
def update_config():
    data = request.json
    for k, v in data.items():
        if k != "adminPassword":
            registry.set(k, v)
    return jsonify({"success": True})

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    if data.get("password") == registry.get("adminPassword"):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Wrong password"}), 401

@app.route("/api/proxy-log")
def proxy_log():
    return jsonify(proxy.get_log())

def _get_user_count(user_id):
    path = "data/transactions.json"
    if not os.path.exists(path): return 0
    with open(path) as f:
        txns = json.load(f)
    return sum(1 for t in txns
               if t["user_id"] == user_id and t["status"] == "SUCCESS")

def _increment_user_count(user_id):
    """No-op: purchase count is tracked via transactions.json by _get_user_count."""
    pass

if __name__ == "__main__":
    app.run(debug=True)