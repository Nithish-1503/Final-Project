// The backend API base URL.
// In Kubernetes this is exposed via the backend Service / Ingress.
// For local docker-compose testing, use http://localhost:5000
const API_BASE = (window.API_BASE || "/api");

const form = document.getElementById("tripForm");
const tripList = document.getElementById("tripList");
const statusEl = document.getElementById("status");

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.style.color = isError ? "#ffd0d0" : "#ffe";
}

async function loadTrips() {
  try {
    const res = await fetch(`${API_BASE}/trips`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const trips = await res.json();
    renderTrips(trips);
    setStatus(`${trips.length} trip(s) loaded.`);
  } catch (err) {
    setStatus("Could not reach backend: " + err.message, true);
  }
}

function renderTrips(trips) {
  tripList.innerHTML = "";
  trips.forEach((t) => {
    const li = document.createElement("li");
    li.className = "trip-card";
    li.innerHTML = `
      <h3>${escapeHtml(t.destination)}</h3>
      <div class="dates">${t.start_date} → ${t.end_date}</div>
      <div class="notes">${escapeHtml(t.notes || "")}</div>
      <button class="del" data-id="${t.id}">Delete</button>
    `;
    tripList.appendChild(li);
  });
  document.querySelectorAll(".del").forEach((btn) => {
    btn.addEventListener("click", () => deleteTrip(btn.dataset.id));
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    destination: document.getElementById("destination").value,
    start_date: document.getElementById("startDate").value,
    end_date: document.getElementById("endDate").value,
    notes: document.getElementById("notes").value,
  };
  try {
    const res = await fetch(`${API_BASE}/trips`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    form.reset();
    setStatus("Trip added!");
    loadTrips();
  } catch (err) {
    setStatus("Failed to add trip: " + err.message, true);
  }
});

async function deleteTrip(id) {
  try {
    const res = await fetch(`${API_BASE}/trips/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    loadTrips();
  } catch (err) {
    setStatus("Failed to delete: " + err.message, true);
  }
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

loadTrips();

