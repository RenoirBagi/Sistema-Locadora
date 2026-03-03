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
const abrirModalExportacaoBtn = document.getElementById("abrir-modal-exportacao");
const modalExportacao = document.getElementById("export-modal");
const fecharModalExportacaoBtn = document.getElementById("fechar-modal-exportacao");
const formExportacao = document.getElementById("form-exportacao");
const exportFeedback = document.getElementById("export-feedback");
const historicoTbody = document.getElementById("historico-tbody");

let seriesChart;
let statusChart;
let topFilmesChart;
let pickerMonth = new Date();
let activeDateInput = null;

function formatDateInput(date) {
  return date.toISOString().split("T")[0];
}

function atualizarHistorico(lista = []) {
  if (!historicoTbody) return;
  historicoTbody.innerHTML = "";

  if (!lista.length) {
    const tr = document.createElement("tr");
    tr.innerHTML = "<td colspan='6'>Nenhuma exportação registrada.</td>";
    historicoTbody.appendChild(tr);
    return;
  }

  lista.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.criado_em}</td>
      <td>${item.tipo_relatorio}</td>
      <td>${item.formato.toUpperCase()}</td>
      <td>${item.periodo}</td>
      <td>${item.total_registros}</td>
      <td>${item.status}</td>
    `;
    historicoTbody.appendChild(tr);
  });
}

async function carregarHistorico(limit = 10) {
  try {
    const resp = await fetch(`${API_URL}/exportacoes/historico?limit=${limit}`);
    if (!resp.ok) throw new Error("Falha ao carregar histórico");
    const dados = await resp.json();
    atualizarHistorico(dados);
  } catch (error) {
    console.error(error);
    if (historicoTbody) {
      historicoTbody.innerHTML = "<tr><td colspan='6'>Erro ao carregar histórico.</td></tr>";
    }
  }
}

function atualizarStatus(status = { ativos: 0, finalizados: 0, percentuais: {} }) {
  document.getElementById("status-ativos").textContent = status.ativos || 0;
  document.getElementById("status-finalizados").textContent = status.finalizados || 0;

  const ctx = document.getElementById("statusChart").getContext("2d");
  if (statusChart) {
    statusChart.destroy();
  }

  const valores = [status.ativos || 0, status.finalizados || 0];
  const total = valores.reduce((acc, curr) => acc + curr, 0);

  const centerTextPlugin = {
    id: "centerText",
    afterDraw(chart) {
      const { ctx: canvasCtx, chartArea } = chart;
      const { width, height, left, top } = chartArea;
      const centerX = left + width / 2;
      const centerY = top + height / 2;

      canvasCtx.save();
      canvasCtx.fillStyle = "#E6EDFF";
      canvasCtx.font = "600 20px 'Poppins', sans-serif";
      canvasCtx.textAlign = "center";
      canvasCtx.textBaseline = "middle";
      canvasCtx.fillText(total || 0, centerX, centerY - 6);

      canvasCtx.fillStyle = "#9AA8C7";
      canvasCtx.font = "500 12px 'Poppins', sans-serif";
      canvasCtx.fillText("Total", centerX, centerY + 12);
      canvasCtx.restore();
    }
  };

  statusChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Ativos", "Finalizados"],
      datasets: [
        {
          data: valores,
          backgroundColor: ["#8FD3FF", "#1E3B70"],
          borderColor: "#101728",
          borderWidth: 2,
          hoverOffset: 6,
          spacing: 4,
          borderRadius: 20
        }
      ]
    },
    options: {
      cutout: "65%",
      plugins: {
        legend: { display: false }
      }
    },
    plugins: [centerTextPlugin]
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

  const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
  gradient.addColorStop(0, "#7895FF");
  gradient.addColorStop(1, "#2747BF");

  topFilmesChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: lista.map(item => item.titulo || "N/D"),
      datasets: [
        {
          label: "Aluguéis",
          data: lista.map(item => item.total_alugueis || 0),
          backgroundColor: gradient,
          borderRadius: { topLeft: 18, topRight: 18, bottomLeft: 6, bottomRight: 6 },
          barPercentage: 0.55,
          categoryPercentage: 0.6,
          borderSkipped: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(5, 8, 20, 0.85)",
          titleFont: { family: "Poppins", weight: "600" },
          bodyFont: { family: "Poppins" },
          callbacks: {
            label: context => `${context.parsed.y || 0} aluguéis`
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: "#B9C6E8",
            maxRotation: 0,
            autoSkip: false,
            font: { size: 11 },
            callback: function (value) {
              const label = this.getLabelForValue(value);
              return wrapLabel(label);
            }
          },
          grid: { display: false }
        },
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
            color: "#8AA0D1"
          },
          grid: { color: "rgba(255,255,255,0.04)" }
        },
        y1: {
          beginAtZero: true,
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: {
            callback: value => formatCurrency(value)
          },
          title: { display: true, text: "Receita", color: "#9FB1D9" }
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

function formatShortDate(dateStr) {
  if (!dateStr) return "-";
  const [year, month, day] = dateStr.split("-");
  return `${day}/${month}`;
}

function wrapLabel(text, maxLen = 14) {
  if (!text) return "";
  const words = text.split(" ");
  const lines = [];
  let current = "";
  words.forEach(word => {
    const testLine = `${current} ${word}`.trim();
    if (testLine.length > maxLen && current) {
      lines.push(current.trim());
      current = word;
    } else {
      current = testLine;
    }
  });
  if (current.trim()) lines.push(current.trim());
  return lines;
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
  const labels = series.map(item => formatShortDate(item.data));
  const alugueis = series.map(item => item.total_alugueis || 0);
  const receitas = series.map(item => Number(item.receita || 0));

  const semDados = series.length === 0;
  seriesEmpty.hidden = !semDados;
  const chartLabels = semDados ? ["Sem dados"] : labels;
  const chartAlugueis = semDados ? [0] : alugueis;
  const chartReceitas = semDados ? [0] : receitas;

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
          label: "Receita",
          data: chartReceitas,
          borderColor: "#1034A6",
          backgroundColor: "rgba(16, 52, 166, 0.25)",
          borderWidth: 3,
          tension: 0.55,
          fill: true,
          pointRadius: 0,
          order: 2,
          yAxisID: "y1"
        },
        {
          label: "Aluguéis",
          data: chartAlugueis,
          borderColor: "#4C8BFF",
          backgroundColor: "rgba(76, 139, 255, 0.35)",
          borderWidth: 3,
          tension: 0.55,
          fill: true,
          pointRadius: 0,
          order: 1,
          yAxisID: "y"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: {
          display: true,
          labels: { usePointStyle: true, color: "#C5D0EC" }
        },
        tooltip: {
          callbacks: {
            label: context => {
              const label = context.dataset.label || "";
              const value = context.parsed.y || 0;
              if (label === "Receita") {
                return `${label}: ${formatCurrency(value)}`;
              }
              return `${label}: ${value} aluguéis`;
            }
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

function abrirModalExportacao() {
  if (!modalExportacao) return;
  const modalInicio = formExportacao?.elements.namedItem("inicio");
  const modalFim = formExportacao?.elements.namedItem("fim");
  if (modalInicio && inicioInput?.value) modalInicio.value = inicioInput.value;
  if (modalFim && fimInput?.value) modalFim.value = fimInput.value;
  modalExportacao.hidden = false;
}

function fecharModalExportacao() {
  if (!modalExportacao) return;
  modalExportacao.hidden = true;
  if (exportFeedback) {
    exportFeedback.hidden = true;
    exportFeedback.textContent = "";
  }
}

async function enviarExportacao(event) {
  event.preventDefault();
  if (!formExportacao) return;

  const payload = {
    tipo: formExportacao.tipo.value,
    formato: formExportacao.formato.value,
    inicio: formExportacao.inicio.value,
    fim: formExportacao.fim.value
  };

  const btn = document.getElementById("btn-confirmar-exportacao");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "Gerando...";
  }

  try {
    const response = await fetch(`${API_URL}/exportacoes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const erro = await response.json().catch(() => ({}));
      throw new Error(erro.erro || "Erro ao gerar relatório");
    }

    const blob = await response.blob();
    const contentDisposition = response.headers.get("Content-Disposition") || "";
    const match = contentDisposition.match(/filename="?([^";]+)"?/i);
    const fileName = match ? match[1] : `relatorio_${Date.now()}.${payload.formato}`;

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);

    fecharModalExportacao();
    carregarHistorico();
  } catch (error) {
    if (exportFeedback) {
      exportFeedback.hidden = false;
      exportFeedback.textContent = error.message || "Falha ao exportar";
    }
    console.error(error);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "Gerar relatório";
    }
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
      fecharModalExportacao();
    }
  });

  abrirModalExportacaoBtn?.addEventListener("click", abrirModalExportacao);
  fecharModalExportacaoBtn?.addEventListener("click", fecharModalExportacao);
  modalExportacao?.addEventListener("click", event => {
    if (event.target === modalExportacao) {
      fecharModalExportacao();
    }
  });
  formExportacao?.addEventListener("submit", enviarExportacao);

  carregarDashboard();
  carregarHistorico();
}

window.addEventListener("DOMContentLoaded", initDashboard);
