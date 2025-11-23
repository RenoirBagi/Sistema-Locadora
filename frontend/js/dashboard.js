const API_URL = "http://localhost:5000";

const formFiltros = document.getElementById("filtros-dashboard");
const inicioInput = formFiltros?.elements.namedItem("inicio");
const fimInput = formFiltros?.elements.namedItem("fim");
const dateInputs = formFiltros?.querySelectorAll('[data-date-input]');
const erroBanner = document.getElementById("dashboard-error");
const topGenerosList = document.getElementById("top-generos-list");
const seriesEmpty = document.getElementById("series-empty");
const topFilmesEmpty = document.getElementById("top-filmes-empty");
const datePicker = document.getElementById("date-picker");
const dpMonthLabel = document.getElementById("dp-month-label");
const dpDays = document.getElementById("dp-days");
const dpPrev = datePicker?.querySelector('[data-action="prev"]');
const dpNext = datePicker?.querySelector('[data-action="next"]');

let seriesChart;
let statusChart; 
let topFilmesChart;
let pickerMonth = new Date();
let activeDateInput = null;

function formatDateInput(date) {
  return date.toISOString().split("T")[0];
}

function atualizarStatus(status = { ativos: 0, finalizados: 0, percentuais: {} }) {
  document.getElementById("status-ativos").textContent = status.ativos || 0;
  document.getElementById("status-finalizados").textContent = status.finalizados || 0;

  const ctx = document.getElementById("statusChart").getContext("2d");
  if (statusChart) {
    statusChart.destroy();
  }

  statusChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Ativos", "Finalizados"],
      datasets: [
        {
          data: [status.ativos || 0, status.finalizados || 0],
          backgroundColor: ["#1DE9B6", "#2979FF"],
          borderWidth: 0,
          hoverOffset: 8
        }
      ]
    },
    options: {
      cutout: "70%",
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function atualizarTopFilmes(lista = []) {
  const ctx = document.getElementById("topFilmesChart").getContext("2d");
  const semDados = !lista.length;
  topFilmesEmpty.hidden = !semDados;

  if (topFilmesChart) {
    topFilmesChart.destroy();
  }

  if (semDados) {
    return;
  }

  topFilmesChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: lista.map(item => item.titulo || "N/D"),
      datasets: [
        {
          label: "Aluguéis",
          data: lista.map(item => item.total_alugueis || 0),
          backgroundColor: "rgba(76, 139, 255, 0.8)",
          borderRadius: 12,
          barThickness: 26
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 }
        }
      }
    }
  });
}

function normalizeDateValue(value) {
  if (!value) return "";
  const trimmed = value.trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) {
    return trimmed;
  }
  const brPattern = /^\d{2}\/\d{2}\/\d{4}$/;
  if (brPattern.test(trimmed)) {
    const [dia, mes, ano] = trimmed.split("/");
    return `${ano}-${mes}-${dia}`;
  }
  const parsed = new Date(trimmed);
  if (!Number.isNaN(parsed.getTime())) {
    return formatDateInput(parsed);
  }
  return "";
}

function formatDisplayDate(dateStr) {
  if (!dateStr) return "-";
  const [year, month, day] = dateStr.split("-");
  return `${day}/${month}/${year}`;
}

function formatCurrency(value) {
  return Number(value || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 2
  });
}

function setDefaultRange() {
  const hoje = new Date();
  const inicio = new Date();
  inicio.setDate(hoje.getDate() - 29);
  if (inicioInput && fimInput) {
    inicioInput.value = formatDateInput(inicio);
    fimInput.value = formatDateInput(hoje);
  }
}

function renderDatePicker() {
  if (!datePicker || !dpMonthLabel || !dpDays) return;
  const ano = pickerMonth.getFullYear();
  const mes = pickerMonth.getMonth();

  const nomeMes = pickerMonth.toLocaleDateString("pt-BR", { month: "long", year: "numeric" });
  dpMonthLabel.textContent = nomeMes.charAt(0).toUpperCase() + nomeMes.slice(1);

  dpDays.innerHTML = "";
  const primeiroDiaSemana = new Date(ano, mes, 1).getDay();
  const diasNoMes = new Date(ano, mes + 1, 0).getDate();

  for (let i = 0; i < primeiroDiaSemana; i += 1) {
    const span = document.createElement("span");
    span.className = "dp-empty";
    dpDays.appendChild(span);
  }

  const valorAtual = normalizeDateValue(activeDateInput?.value || "");

  for (let dia = 1; dia <= diasNoMes; dia += 1) {
    const button = document.createElement("button");
    button.type = "button";
    const data = new Date(ano, mes, dia);
    const iso = formatDateInput(data);
    button.dataset.date = iso;
    button.textContent = String(dia);
    if (valorAtual === iso) {
      button.classList.add("dp-day--selected");
    }
    button.addEventListener("click", () => {
      if (activeDateInput) {
        activeDateInput.value = iso;
        activeDateInput.dispatchEvent(new Event("change"));
      }
      closeDatePicker();
    });
    dpDays.appendChild(button);
  }
}

function positionDatePicker(input) {
  if (!datePicker) return;
  const rect = input.getBoundingClientRect();
  const top = window.scrollY + rect.bottom + 8;
  const left = window.scrollX + rect.left;
  datePicker.style.top = `${top}px`;
  datePicker.style.left = `${left}px`;
}

function openDatePicker(input) {
  if (!datePicker) return;
  activeDateInput = input;
  const dataAtual = normalizeDateValue(input.value);
  pickerMonth = dataAtual ? new Date(dataAtual) : new Date();
  datePicker.hidden = false;
  positionDatePicker(input);
  renderDatePicker();
}

function closeDatePicker() {
  if (!datePicker) return;
  datePicker.hidden = true;
  activeDateInput = null;
}

async function carregarDashboard(event) {
  if (event) event.preventDefault();
  if (!inicioInput || !fimInput) return;

  const inicioValor = normalizeDateValue(inicioInput.value);
  const fimValor = normalizeDateValue(fimInput.value);

  if (!inicioValor || !fimValor) {
    toggleError("Informe datas válidas no formato DD/MM/AAAA ou AAAA-MM-DD.");
    return;
  }

  inicioInput.value = inicioValor;
  fimInput.value = fimValor;

  const params = new URLSearchParams({
    inicio: inicioValor,
    fim: fimValor
  });

  const resumoUrl = `${API_URL}/dashboard/resumo?${params}`;
  const seriesUrl = `${API_URL}/dashboard/series?${params}`;
  const generosUrl = `${API_URL}/dashboard/top-generos?${params}&limit=5`;
  const statusUrl = `${API_URL}/dashboard/status?${params}`;
  const topFilmesUrl = `${API_URL}/dashboard/top-filmes?${params}&limit=5`;

  try {
    toggleError();
    const [resumoResp, seriesResp, generosResp, statusResp, topFilmesResp] = await Promise.all([
      fetch(resumoUrl),
      fetch(seriesUrl),
      fetch(generosUrl),
      fetch(statusUrl),
      fetch(topFilmesUrl)
    ]);

    if (!resumoResp.ok || !seriesResp.ok || !generosResp.ok || !statusResp.ok || !topFilmesResp.ok) {
      throw new Error("Falha ao carregar dados do dashboard");
    }

    const [resumo, series, topGeneros, status, topFilmes] = await Promise.all([
      resumoResp.json(),
      seriesResp.json(),
      generosResp.json(),
      statusResp.json(),
      topFilmesResp.json()
    ]);

    atualizarResumo(resumo);
    atualizarSeries(series);
    atualizarTopGeneros(topGeneros);
    atualizarStatus(status);
    atualizarTopFilmes(topFilmes);
  } catch (error) {
    console.error(error);
    toggleError("Não foi possível carregar os dados. Tente novamente.");
  }
}

function atualizarResumo({ total_alugueis = 0, receita_total = 0, ticket_medio = 0, periodo = {} } = {}) {
  document.getElementById("kpi-total").textContent = total_alugueis;
  document.getElementById("kpi-receita").textContent = formatCurrency(receita_total);
  document.getElementById("kpi-ticket").textContent = formatCurrency(ticket_medio);
  document.getElementById("kpi-periodo").textContent = periodo.inicio && periodo.fim
    ? `Período: ${formatDisplayDate(periodo.inicio)} – ${formatDisplayDate(periodo.fim)}`
    : "";
}

function atualizarSeries(series = []) {
  const labels = series.map(item => formatDisplayDate(item.data));
  const alugueis = series.map(item => item.total_alugueis || 0);

  const semDados = series.length === 0;
  seriesEmpty.hidden = !semDados;
  const chartLabels = semDados ? ["Sem dados"] : labels;
  const chartAlugueis = semDados ? [0] : alugueis;

  const ctx = document.getElementById("seriesChart").getContext("2d");
  if (seriesChart) {
    seriesChart.destroy();
  }

  seriesChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: chartLabels,
      datasets: [
        {
          label: "Aluguéis",
          data: chartAlugueis,
          borderColor: "#4C8BFF",
          backgroundColor: "rgba(76, 139, 255, 0.15)",
          borderWidth: 3,
          tension: 0.5,
          fill: true,
          pointRadius: 5,
          pointBackgroundColor: "#FFFFFF",
          pointBorderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: context => `${context.parsed.y} aluguéis`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 }
        }
      }
    }
  });
}

function atualizarTopGeneros(lista = []) {
  if (!topGenerosList) return;
  topGenerosList.innerHTML = "";

  if (!lista.length) {
    topGenerosList.innerHTML = "<li>Nenhum gênero no período.</li>";
    return;
  }

  lista.forEach((item, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${index + 1}. ${item.genero || "N/D"}</span>
      <strong>${item.total_alugueis || 0}</strong>
    `;
    topGenerosList.appendChild(li);
  });
}

function toggleError(message = "") {
  if (!erroBanner) return;
  if (message) {
    erroBanner.textContent = message;
    erroBanner.hidden = false;
  } else {
    erroBanner.hidden = true;
    erroBanner.textContent = "";
  }
}

function initDashboard() {
  if (!formFiltros) return;
  setDefaultRange();
  formFiltros.addEventListener("submit", carregarDashboard);

  dateInputs?.forEach(input => {
    input.addEventListener("focus", () => openDatePicker(input));
    input.addEventListener("click", () => openDatePicker(input));
  });

  dpPrev?.addEventListener("click", () => {
    pickerMonth.setMonth(pickerMonth.getMonth() - 1);
    renderDatePicker();
  });

  dpNext?.addEventListener("click", () => {
    pickerMonth.setMonth(pickerMonth.getMonth() + 1);
    renderDatePicker();
  });

  document.addEventListener("click", event => {
    if (!datePicker || datePicker.hidden) return;
    const target = event.target;
    if (target === activeDateInput || datePicker.contains(target)) {
      return;
    }
    closeDatePicker();
  });

  document.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      closeDatePicker();
    }
  });

  carregarDashboard();
}

window.addEventListener("DOMContentLoaded", initDashboard);
