# Aura Retail OS

**Course:** IT620 — Object Oriented Programming  
**Team:** Binary Bros (Path B — Modular Hardware Platform)

| Name | Role | Subsystem |
|------|------|-----------|
| Nirav Kachhiya | Group Lead | Hardware Abstraction Layer |
| Akshay Purohit | Member | Payment System Integration |
| Achyut Pathak | Member | Inventory & Kiosk Core |
| Jainam Shah | Member | Secure Access & Modules |

---

## Overview

Aura Retail OS is a modular, pattern-driven vending kiosk platform built entirely in Python. It supports multiple kiosk types (Food, Pharmacy, Emergency Relief), swappable hardware dispensers, multiple payment providers, and a web-based admin dashboard — all demonstrating 8 Gang-of-Four design patterns.

---

## Design Patterns Implemented

| # | Pattern | Type | Implementation |
|---|---------|------|----------------|
| 1 | **Singleton** | Creational | `CentralRegistry` — single config instance across all kiosks |
| 2 | **Factory Method** | Creational | `KioskFactory` — creates FoodKiosk / PharmacyKiosk / EmergencyReliefKiosk |
| 3 | **Composite** | Structural | `ProductBundle` — treats individual products and bundles uniformly via `IInventoryItem` |
| 4 | **Adapter** | Structural | `CreditCardAdapter`, `UPIAdapter`, `DigitalWalletAdapter` — unify different payment APIs |
| 5 | **Proxy** | Structural | `SecureInventoryProxy` — access control and logging layer over `InventoryManager` |
| 6 | **Decorator** | Structural | `RefrigerationModule`, `SolarMonitorModule` — attach/detach hardware modules dynamically |
| 7 | **Strategy** | Behavioral | `IDispenser` — swap between SpiralDispenser, RoboticArmDispenser, ConveyorDispenser at runtime |
| 8 | **Command** | Behavioral | `PurchaseItemCommand`, `RefundCommand`, `RestockCommand` — encapsulate operations with undo support |

---

## Project Structure

```
aura-retail-os/
├── app.py                          # Flask web server
├── simulation.py                   # CLI simulation demo
├── data/
│   ├── config.json                 # Singleton registry config
│   ├── inventory.json              # Product data
│   └── transactions.json           # Transaction history
├── src/
│   ├── registry/
│   │   └── central_registry.py     # Singleton Pattern
│   ├── inventory/
│   │   ├── i_inventory_item.py     # Component interface (Composite)
│   │   ├── product.py              # Leaf (Composite)
│   │   ├── product_bundle.py       # Composite (Composite)
│   │   └── inventory_manager.py    # Inventory storage
│   ├── payment/
│   │   ├── i_payment_processor.py  # Target interface (Adapter)
│   │   ├── credit_card_adapter.py  # Adapter
│   │   ├── credit_card_gateway.py  # Adaptee
│   │   ├── upi_adapter.py          # Adapter
│   │   └── digital_wallet_adapter.py # Adapter
│   ├── hardware/
│   │   ├── i_dispenser.py          # Strategy interface
│   │   ├── spiral_dispenser.py     # Concrete Strategy
│   │   ├── robotic_arm_dispenser.py # Concrete Strategy
│   │   ├── conveyor_dispenser.py   # Concrete Strategy
│   │   ├── i_hardware_module.py    # Decorator interface
│   │   ├── refrigeration_module.py # Concrete Decorator
│   │   └── solar_monitor_module.py # Concrete Decorator
│   ├── kiosks/
│   │   ├── abstract_kiosk.py       # Abstract product (Factory)
│   │   ├── food_kiosk.py           # Concrete product
│   │   ├── pharmacy_kiosk.py       # Concrete product
│   │   ├── emergency_relief_kiosk.py # Concrete product
│   │   ├── kiosk_factory.py        # Factory Method
│   │   └── kiosk_interface.py      # Facade
│   ├── commands/
│   │   ├── i_command.py            # Command interface
│   │   ├── purchase_item_command.py # Concrete Command
│   │   ├── refund_command.py       # Concrete Command
│   │   └── restock_command.py      # Concrete Command
│   └── security/
│       └── secure_inventory_proxy.py # Proxy Pattern
├── templates/
│   └── index.html                  # Web UI
└── static/
    ├── app.js                      # Frontend logic
    └── style.css                   # Styling
```

---

## How to Run

### Prerequisites
- Python 3.10+
- Flask (`pip install flask`)

### Option 1: CLI Simulation
```bash
python simulation.py
```

### Option 2: Web Application
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`

---

## Simulation Demonstration

### Step 1 — Start the System
```
python simulation.py
```
Output:
```
================================================
  AURA RETAIL OS — Interactive Simulation
================================================
  Location : Metro Station - Block A
  Currency : INR

  ---- Login ----
  1. User
  2. Admin
  3. Exit System
```

### Step 2 — User Login & Purchase
1. Select `1` (User)
2. Enter your name (e.g., `Nirav`)
3. Select `1` to buy Water Bottle (₹20)
4. Observe: CreditCardGateway charges ₹20, SpiralDispenser dispenses P001

```
  [CreditCardGateway] Charging ₹20.0 to: Nirav
  [SpiralDispenser] Dispensing P001
```

### Step 3 — Attempt Out-of-Stock Purchase
1. Keep buying Water Bottles until stock reaches 0
2. Observe the purchase fails gracefully

### Step 4 — Admin Login
1. Logout, then select `2` (Admin)
2. Enter password: `admin123`
3. View inventory, transaction history, and payment summary
4. Restock a product and verify updated stock

### Step 5 — Change Kiosk Location
1. In admin panel, select `5` (Change Location)
2. Enter a new location (Singleton pattern updates everywhere)

---

## Web App Features

- **User Shop** — Browse products, purchase items with real-time stock updates
- **Admin Panel** — Inventory management, transaction history, restock, refunds
- **Kiosk Configuration** — Switch kiosk type, dispenser, and payment provider at runtime
- **Hardware Modules** — Attach/detach refrigeration and solar modules (Decorator)
- **Proxy Log** — View all inventory access logs (Proxy pattern)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | System status |
| GET | `/api/products` | List all products |
| POST | `/api/purchase` | Purchase a product |
| POST | `/api/refund` | Refund a transaction |
| POST | `/api/restock` | Restock a product |
| GET | `/api/transactions` | Transaction history |
| POST | `/api/switch-kiosk` | Change kiosk/dispenser/payment |
| POST | `/api/module` | Attach/detach hardware module |
| GET | `/api/config` | Get configuration |
| PUT | `/api/config` | Update configuration |
| GET | `/api/proxy-log` | Proxy access log |
