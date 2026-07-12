"use strict";

const INDICATOR_LABELS = {
  devoluciones: "Devoluciones",
  deuda: "Deuda",
  codigos_propios: "Códigos propios",
  pvp: "Cambios de PVP",
  recetas: "Recetas",
  stock: "Stock",
};

const $ = (sel) => document.querySelector(sel);

// ---------- Estado de la API ----------
async function checkApi() {
  const dot = $("#status-dot");
  const text = $("#status-text");
  try {
    const res = await fetch("/health");
    if (!res.ok) throw new Error();
    dot.classList.add("ok");
    text.textContent = "API operativa";
  } catch {
    dot.classList.add("ko");
    text.textContent = "API no disponible";
  }
}

// ---------- Utilidades de UI ----------
function selectedIndicators() {
  return [...document.querySelectorAll('.indicators input[type="checkbox"]:checked')].map(
    (cb) => cb.value
  );
}

function showError(message) {
  const box = $("#error-box");
  box.textContent = message;
  box.classList.remove("hidden");
}

function clearError() {
  $("#error-box").classList.add("hidden");
}

function setLoading(loading, label = "Generando informes…") {
  $("#run-btn").disabled = loading;
  const progress = $("#progress");
  $("#progress-text").textContent = label;
  progress.classList.toggle("hidden", !loading);
}

// ---------- Render de resultados ----------
let currentAxId = null;

function renderReports(data) {
  $("#empty-state").classList.add("hidden");
  $("#results-meta").textContent = `Análisis ${data.ax_id} · ${data.reports.length} indicador(es)`;

  currentAxId = data.ax_id;

  const container = $("#reports");
  container.innerHTML = "";

  data.reports.forEach((report) => {
    const label = INDICATOR_LABELS[report.indicator] || report.indicator;
    const card = document.createElement("div");
    card.className = "report";
    card.dataset.indicator = report.indicator;
    card.innerHTML = `
      <div class="report-head">
        <span class="report-title">${label}</span>
        <span class="badge" data-badge>Pendiente de revisión</span>
      </div>
      <textarea rows="8"></textarea>
      <div class="report-actions">
        <button type="button" class="ghost" data-validate>Marcar como válido</button>
      </div>`;
    card.querySelector("textarea").value = report.text;

    const badge = card.querySelector("[data-badge]");
    card.querySelector("[data-validate]").addEventListener("click", () => {
      const valid = badge.classList.toggle("valid");
      badge.textContent = valid ? "Validado" : "Pendiente de revisión";
    });

    container.appendChild(card);
  });

  $("#conclusion-text").value = data.conclusion;
  $("#conclusion-block").classList.remove("hidden");
  $("#results-actions").classList.remove("hidden");
}

function collectFullReport() {
  let out = "";
  document.querySelectorAll(".report").forEach((card) => {
    const title = card.querySelector(".report-title").textContent;
    const text = card.querySelector("textarea").value;
    out += `### ${title}\n${text}\n\n`;
  });
  out += `### Conclusión global\n${$("#conclusion-text").value}\n`;
  return out;
}

function collectValidationPayload() {
  const reports = [...document.querySelectorAll(".report")].map((card) => ({
    indicator: card.dataset.indicator,
    text: card.querySelector("textarea").value,
  }));
  return { ax_id: currentAxId, reports, conclusion: $("#conclusion-text").value };
}

// ---------- Validar y guardar en la base de datos ----------
async function saveValidated() {
  clearError();
  const btn = $("#save-btn");
  btn.disabled = true;
  btn.textContent = "Guardando…";

  try {
    const res = await fetch("/conclusions/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collectValidationPayload()),
    });

    if (!res.ok) {
      const detail = await res.text();
      throw new Error(`Error ${res.status}: ${detail}`);
    }

    document.querySelectorAll("[data-badge]").forEach((badge) => {
      badge.classList.add("valid");
      badge.textContent = "Validado";
    });
    btn.textContent = "Guardado ✓";
    setTimeout(() => {
      btn.textContent = "Validar y guardar";
      btn.disabled = false;
    }, 2000);
  } catch (err) {
    showError(err.message || "No se pudo guardar el informe.");
    btn.textContent = "Validar y guardar";
    btn.disabled = false;
  }
}

// ---------- Lanzar el proceso ----------
async function generate(event) {
  event.preventDefault();
  clearError();

  const axId = $("#ax_id").value.trim();
  const indicators = selectedIndicators();

  if (!axId) return showError("Introduce un identificador de análisis (ax_id).");
  if (indicators.length === 0) return showError("Selecciona al menos un indicador.");

  setLoading(true);
  try {
    const res = await fetch("/conclusions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ax_id: axId, indicators }),
    });

    if (!res.ok) {
      const detail = await res.text();
      throw new Error(`Error ${res.status}: ${detail}`);
    }

    renderReports(await res.json());
  } catch (err) {
    showError(err.message || "Se produjo un error durante la generación.");
  } finally {
    setLoading(false);
  }
}

// ---------- Eventos ----------
function init() {
  checkApi();
  $("#conclusion-form").addEventListener("submit", generate);

  $("#select-all").addEventListener("click", () => {
    const boxes = document.querySelectorAll('.indicators input[type="checkbox"]');
    const allChecked = [...boxes].every((cb) => cb.checked);
    boxes.forEach((cb) => (cb.checked = !allChecked));
    $("#select-all").textContent = allChecked ? "Seleccionar todos" : "Quitar todos";
  });

  $("#save-btn").addEventListener("click", saveValidated);

  $("#copy-btn").addEventListener("click", async () => {
    await navigator.clipboard.writeText(collectFullReport());
    $("#copy-btn").textContent = "Copiado ✓";
    setTimeout(() => ($("#copy-btn").textContent = "Copiar todo"), 1500);
  });

  $("#download-btn").addEventListener("click", () => {
    const blob = new Blob([collectFullReport()], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `informe_${$("#ax_id").value.trim() || "analisis"}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  });
}

document.addEventListener("DOMContentLoaded", init);
