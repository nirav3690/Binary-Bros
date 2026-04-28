let currentUser = null;
let selectedItem = null;
let isAdmin = false;
let systemStatus = {};

window.onload = () => {
    fetchStatus();
    setInterval(fetchStatus, 10000);
};

async function fetchStatus() {
    const res = await fetch("/api/status");
    systemStatus = await res.json();
    document.getElementById("location-badge").textContent = systemStatus.location;
    document.getElementById("kiosk-badge").textContent =
        systemStatus.kioskType.charAt(0).toUpperCase() + systemStatus.kioskType.slice(1) + " Kiosk";
}

function userLogin() {
    const name = document.getElementById("username-input").value.trim();
    if (!name) return alert("Please enter your name");
    currentUser = name;
    document.getElementById("display-name").textContent = name;
    showScreen("shop-screen");
    loadProducts();
}

function logout() {
    currentUser = null;
    document.getElementById("username-input").value = "";
    showScreen("login-screen");
}

function showScreen(id) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

async function loadProducts() {
    await fetchStatus();
    const res = await fetch("/api/products");
    const products = await res.json();

    document.getElementById("shop-kiosk-type").textContent =
        systemStatus.kioskType.charAt(0).toUpperCase() + systemStatus.kioskType.slice(1) + " Kiosk";
    document.getElementById("shop-dispenser").textContent = systemStatus.dispenser;
    document.getElementById("shop-payment").textContent =
        systemStatus.payment.charAt(0).toUpperCase() + systemStatus.payment.slice(1) + " Payment";

    const grid = document.getElementById("products-grid");
    grid.innerHTML = "";
    products.forEach(p => {
        const badge = p.stock === 0 ? "out" : p.stock < 3 ? "low" : "";
        const badgeText = p.stock === 0 ? "Out of Stock" : p.stock < 3 ? "Low Stock" : `${p.stock} in stock`;
        const card = document.createElement("div");
        card.className = `product-card ${!p.available ? "unavailable" : ""}`;
        card.innerHTML = `
      <div class="product-name">${p.name}</div>
      <div class="product-price">₹${p.price}</div>
      <div class="product-stock">ID: ${p.id}</div>
      <span class="stock-badge ${badge}">${badgeText}</span>`;
        if (p.available) {
            card.onclick = () => openPurchaseModal(p);
        }
        grid.appendChild(card);
    });
}

function openPurchaseModal(product) {
    selectedItem = product;
    document.getElementById("modal-product-name").textContent = product.name;
    document.getElementById("modal-product-price").textContent = `Price: ₹${product.price}`;
    document.getElementById("modal-payment-info").textContent =
        `Payment via: ${systemStatus.payment.toUpperCase()}`;
    document.getElementById("purchase-result").className = "";
    document.getElementById("purchase-result").style.display = "none";
    document.getElementById("modal-action-btns").style.display = "flex";
    document.getElementById("confirm-purchase-btn").onclick = confirmPurchase;
    const modal = document.getElementById("purchase-modal");
    modal.classList.add("active");
    modal.onclick = (e) => { if (e.target === modal) closePurchaseModal(); };
}

function closePurchaseModal() {
    document.getElementById("purchase-modal").classList.remove("active");
    // Reset modal for next use
    document.getElementById("modal-action-btns").style.display = "flex";
    document.getElementById("modal-close-btn").style.display = "none";
    document.getElementById("purchase-result").style.display = "none";
    document.getElementById("purchase-result").className = "";
    selectedItem = null;
    loadProducts();
}

async function confirmPurchase() {
    if (!selectedItem || !currentUser) return;
    document.getElementById("modal-action-btns").style.display = "none";
    try {
        const res = await fetch("/api/purchase", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: selectedItem.id, user_id: currentUser })
        });
        const data = await res.json();
        const el = document.getElementById("purchase-result");
        el.textContent = data.message || (data.success ? "Purchase successful" : "Purchase failed");
        el.className = data.success ? "success" : "error";
        el.style.display = "block";
    } catch (err) {
        console.error("Purchase error:", err);
        const el = document.getElementById("purchase-result");
        el.textContent = "Something went wrong: " + err.message;
        el.className = "error";
        el.style.display = "block";
    }
    // Always show the close button, even if the API call failed
    document.getElementById("modal-close-btn").style.display = "inline-block";
}

function openAdmin() {
    if (isAdmin) {
        showScreen("admin-screen");
        loadAdminData();
    } else {
        document.getElementById("admin-modal").classList.add("active");
    }
}

function closeAdminModal() {
    document.getElementById("admin-modal").classList.remove("active");
    document.getElementById("admin-password").value = "";
    document.getElementById("admin-error").textContent = "";
}

async function adminLogin() {
    const pass = document.getElementById("admin-password").value;
    const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: pass })
    });
    if (res.ok) {
        isAdmin = true;
        closeAdminModal();
        showScreen("admin-screen");
        loadAdminData();
    } else {
        document.getElementById("admin-error").textContent = "Wrong password";
    }
}

function closeAdmin() {
    showScreen(currentUser ? "shop-screen" : "login-screen");
}

async function loadAdminData() {
    await fetchStatus();
    loadAdminProducts();
    loadTransactions();
    loadModuleStatus();
    loadProxyLog();
    document.getElementById("kiosk-type-select").value = systemStatus.kioskType;
    document.getElementById("dispenser-select").value = systemStatus.dispenser.toLowerCase().split(" ")[0];
    document.getElementById("payment-select").value = systemStatus.payment;
    const cfg = await (await fetch("/api/config")).json();
    document.getElementById("location-input").value = cfg.kioskLocation || "";
}

async function loadAdminProducts() {
    const res = await fetch("/api/products");
    const products = await res.json();
    const div = document.getElementById("admin-products");
    div.innerHTML = `<div class="admin-product-row header">
    <span>Name</span><span>Price</span><span>Stock</span><span>Status</span><span>Restock</span></div>`;
    products.forEach(p => {
        const row = document.createElement("div");
        row.className = "admin-product-row";
        row.innerHTML = `
      <span>${p.name}</span>
      <span>₹${p.price}</span>
      <span>${p.stock}</span>
      <span class="stock-badge ${p.stock === 0 ? "out" : p.stock < 3 ? "low" : ""}">
        ${p.stock === 0 ? "Out" : p.stock < 3 ? "Low" : "OK"}</span>
      <span>
        <input class="restock-input" type="number" min="1" value="5" id="qty-${p.id}">
        <button class="restock-btn" onclick="restock('${p.id}')">Restock</button>
      </span>`;
        div.appendChild(row);
    });
}

async function restock(productId) {
    const qty = parseInt(document.getElementById(`qty-${productId}`).value);
    const res = await fetch("/api/restock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_id: productId, quantity: qty })
    });
    const data = await res.json();
    alert(data.message);
    loadAdminProducts();
}

async function loadTransactions() {
    const res = await fetch("/api/transactions");
    const txns = await res.json();
    const total = txns.filter(t => t.status === "SUCCESS").reduce((s, t) => s + t.amount, 0);
    const success = txns.filter(t => t.status === "SUCCESS").length;
    const failed = txns.filter(t => t.status === "FAILED").length;
    const refunded = txns.filter(t => t.status === "REFUNDED").length;

    document.getElementById("txn-summary").innerHTML = `
    <div class="txn-card"><div class="num">${txns.length}</div><div class="label">Total</div></div>
    <div class="txn-card"><div class="num">${success}</div><div class="label">Successful</div></div>
    <div class="txn-card"><div class="num">${failed}</div><div class="label">Failed</div></div>
    <div class="txn-card"><div class="num">${refunded}</div><div class="label">Refunded</div></div>
    <div class="txn-card"><div class="num">₹${total.toFixed(2)}</div><div class="label">Revenue</div></div>`;

    const list = document.getElementById("transactions-list");
    list.innerHTML = `<div class="txn-row header">
    <span>Txn ID</span><span>Product</span><span>User</span>
    <span>Amount</span><span>Time</span><span>Status</span></div>`;
    [...txns].reverse().forEach(t => {
        const row = document.createElement("div");
        row.className = "txn-row";
        const badgeClass = t.status === "SUCCESS" ? "badge-success" :
            t.status === "REFUNDED" ? "badge-refunded" : "badge-failed";
        const refundBtn = t.status === "SUCCESS" ?
            `<button class="refund-btn" onclick="refund('${t.txn_id}')">Refund</button>` : "";
        row.innerHTML = `
      <span style="font-size:11px;font-family:monospace">${t.txn_id}</span>
      <span>${t.product_id}</span><span>${t.user_id}</span>
      <span>₹${t.amount}</span><span style="font-size:11px">${t.timestamp}</span>
      <span><span class="${badgeClass}">${t.status}</span> ${refundBtn}</span>`;
        list.appendChild(row);
    });
}

async function refund(txnId) {
    if (!confirm("Refund this transaction?")) return;
    const res = await fetch("/api/refund", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ txn_id: txnId })
    });
    const data = await res.json();
    alert(data.message);
    loadTransactions();
}

async function applyKioskConfig() {
    const kioskType = document.getElementById("kiosk-type-select").value;
    const dispenser = document.getElementById("dispenser-select").value;
    const payment = document.getElementById("payment-select").value;
    const location = document.getElementById("location-input").value;

    await fetch("/api/switch-kiosk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kiosk_type: kioskType, dispenser, payment })
    });
    if (location) {
        await fetch("/api/config", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ kioskLocation: location })
        });
    }
    await fetchStatus();
    const msg = document.getElementById("config-msg");
    msg.textContent = "Configuration applied successfully!";
    msg.className = "success";
    setTimeout(() => { msg.className = ""; }, 3000);
    if (currentUser) loadProducts();
}

async function toggleModule(module, action) {
    const res = await fetch("/api/module", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ module, action })
    });
    const data = await res.json();
    loadModuleStatus();
}

async function loadModuleStatus() {
    const res = await fetch("/api/status");
    const data = await res.json();
    ["refrig", "solar"].forEach((key, i) => {
        const modKey = i === 0 ? "refrigeration" : "solar";
        const el = document.getElementById(`${key}-status`);
        const status = data.modules[modKey];
        el.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        el.className = `status-badge ${status === "inactive" ? "inactive" : "active"}`;
    });
}

async function loadProxyLog() {
    const res = await fetch("/api/proxy-log");
    const logs = await res.json();
    const div = document.getElementById("proxy-log-list");
    div.innerHTML = logs.length ? logs.map(l => `<div>${l}</div>`).join("") : "<div>No activity yet.</div>";
}

function showTab(tabId, btn) {
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.getElementById(tabId).classList.add("active");
    btn.classList.add("active");
    if (tabId === "proxy-tab") loadProxyLog();
    if (tabId === "transactions-tab") loadTransactions();
    if (tabId === "inventory-tab") loadAdminProducts();
    if (tabId === "modules-tab") loadModuleStatus();
}